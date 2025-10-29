#!/usr/bin/python

# Copyright Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# core logic borrowed from https://github.com/openstack-k8s-operators/openstack-must-gather/blob/main/pyscripts/mask.py
# and modified to a module according to our requirement
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: crawl_n_mask

short_description: This module mask secrets in yaml/json/log files/dirs

version_added: "1.0.0"

description:
    - This module crawls over a directory (default) and find yaml/json/log files which may have secrets in it, and proceeds with masking it.
    - If you pass a yaml/json/log file, it will directly check and mask secret in it.
    - If you pass a directory, it will crawl the directory and find eligible files to mask.
    - For log files, it optimizes for large files with long lines and sparse secrets. Optimizied by checking first keywords in each line
      (C implementation) and then moving to apply expensive regexps, in the lines with sparsed secrets. This also helps with long lines.

options:
    path:
        description:
            - This is the target file/dir you want to mask.
        required: true
        type: path
    isdir:
        description:
            - Tells if the path is dir or not.
            - Supported options are True and False.
            - Set value to False if path is file, else True.
            - Defaults to False.
        required: false
        default: False
        type: bool

author:
    - Amartya Sinha (@amartyasinha)
"""

EXAMPLES = r"""
- name: Mask secrets in all yaml/json/log files within /home/zuul/logs
  crawl_n_mask:
    path: /home/zuul/logs
    isdir: True

- name: Mask my_secrets.yaml
  crawl_n_mask:
    path: /home/zuul/logs/my_secrets.yaml

- name: Mask application.log
  crawl_n_mask:
    path: /var/log/application.log
"""

RETURN = r"""
success:
    description: Status of the execution
    type: bool
    returned: always
    sample: true
"""

import os
import re
import pathlib

from ansible.module_utils.basic import AnsibleModule

# ### To debug ###
# #  playbook:
#    ---
#    - name: test
#      hosts: localhost
#      tasks:
#        - name: Mask secrets in yaml log files
#          timeout: 3600
#          crawl_n_mask:
#            path: "/tmp/logs/"
#            isdir: true
#
# # args.json:
#   {"ANSIBLE_MODULE_ARGS": {"path": "/tmp/logs/", "isdir": true}}
#
# # execute:
#   python3 plugins/modules/crawl_n_mask.py ./args.json
################

# files which are yaml but do not end with .yaml or .yml
ALLOWED_YAML_FILES = [
    "Standalone",
]
# dirs which we do not want to scan
EXCLUDED_DIRS = [
    "openstack-k8s-operators-openstack-must-gather",
    "tmp",
    "venv",
    ".github",
]
# Used to skip Ansible task headers from txt/log masked files
ANSIBLE_SKIP_PATTERNS = [
    "| TASK [",  # Ansible task header
    "TASK: ",  # Alternative format
    "PLAY [",  # Ansible play header
]
# File extensions which we do not want to process
EXCLUDED_FILE_EXT = [
    ".py",
    ".html",
    ".DS_Store",
    ".tar.*",
    ".gz",
    ".rpm",
    ".zip",
    ".j2",
]
# keys in files whose values need to be masked
PROTECT_KEYS = [
    "literals",
    "PASSWORD",
    "Password",
    "password",
    "_pwd",
    "_PWD",
    "Token",
    "Secret",
    "secret",
    "SECRET",
    "Authkey",
    "authkey",
    "private_key",
    "privatekey",
    "Passphrase",
    "passphrase",
    "PASSPHRASE",
    "encryption_key",
    "ENCRYPTION_KEY",
    "HeatAuthEncryptionKey",
    "oc_login_command",
    "METADATA_SHARED_SECRET",
    "KEYSTONE_FEDERATION_CLIENT_SECRET",
    "rabbit",
    "database_connection",
    "slave_connection",
    "sql_connection",
    "cifmw_openshift_login_password",
    "cifmw_openshift_login_token",
    "BarbicanSimpleCryptoKEK",
    "OctaviaHeartbeatKey",
    "server-ca-passphrase",
    "KeystoneFernetKeys",
    "KeystoneFernetKey",
    "KeystoneCredential",
    "DesignateRndcKey",
    "CephRgwKey",
    "CephClusterFSID",
    "CephClientKey",
    "BarbicanSimpleCryptoKek",
    "BARBICAN_SIMPLE_CRYPTO_ENCRYPTION_KEY",
    "HashSuffix",
    "RabbitCookie",
    "erlang_cookie",
    "ClientKey",
    "swift_store_key",
    "secret_key",
    "heartbeat_key",
    "fernet_keys",
    "sshkey",
    "keytab_base64",
    "cifmw_openshift_token",
]
# connection keys which may be part of the value itself
CONNECTION_KEYS = [
    "rabbit",
    "database_connection",
    "slave_connection",
    "sql_connection",
]
# Masking string
MASK_STR = "**********"

# regex of excluded file extensions
excluded_file_ext_regex = r"(^.*(%s).*)" % "|".join(EXCLUDED_FILE_EXT)

# Lowering case here to enhance performance
# PROTECT_KEYS should be case sensitive to proper mask json and yaml files
# TODO(evallesp: Refactor JSON/YAML format to use this QUICK_KEYWORDS
QUICK_KEYWORDS = frozenset([key.lower() for key in PROTECT_KEYS])

# Pre-compiled regex patterns for log file masking. Increased performance.
LOG_PATTERNS = {
    # Python dict style with quoted keys and values
    # Matches: 'password': 'value', "token": "value"
    "python_dict_quoted": re.compile(
        r"(['\"])("
        + "|".join(PROTECT_KEYS)
        + r")(['\"])\s*:\s*(['\"])([^'\"]+)(['\"])",
        re.IGNORECASE,
    ),
    # Python dict with quoted keys, numeric values
    # Matches: 'password': 123456789
    "python_dict_numeric": re.compile(
        r"(['\"])(" + "|".join(PROTECT_KEYS) + r")(['\"])\s*:\s*(\d{6,})", re.IGNORECASE
    ),
    # Plain KEY:VALUE or KEY=VALUE (YAML/config style)
    # Matches: password: value, token=value, password : value
    "plain_key_value": re.compile(
        r"\b(" + "|".join(PROTECT_KEYS) + r')\s*[:=]\s*["\']?([^\s"\',}\]]{3,})["\']?',
        re.IGNORECASE,
    ),
    # SHA256 tokens (OpenShift style)
    # Matches: sha256~...
    "sha256_token": re.compile(r"sha256~[A-Za-z0-9_-]+"),
    # Bearer tokens
    # Matches: Bearer <token>
    "bearer": re.compile(r"Bearer\s+[a-zA-Z0-9_-]{20,}", re.IGNORECASE),
    # Connection strings with credentials
    # Matches: ://user:pass@host
    "connection_string": re.compile(
        r"://([a-zA-Z0-9_-]+):([a-zA-Z0-9_@!#$%^&*]+)@([a-zA-Z0-9.-]+)"
    ),
}


def handle_walk_errors(e):
    raise e


def crawl(module, path) -> bool:
    """
    Crawler function which will crawl through the log directory
    and find eligible files for masking.
    """
    changed = False
    base_path = os.path.normpath(path)
    for root, _, files in os.walk(base_path, onerror=handle_walk_errors):
        # Get relative path from our base path
        rel_path = os.path.relpath(root, base_path)

        # Check if any parent directory (not the root) is excluded
        if any(part in EXCLUDED_DIRS for part in rel_path.split(os.sep)):
            continue
        for f in files:
            if not re.search(excluded_file_ext_regex, f):
                if mask(module, os.path.join(root, f)):
                    # even if one file is masked, the final result will be True
                    changed = True
    return changed


def _get_masked_string(value):
    if len(value) <= 4:
        return value[:2] + MASK_STR
    return value[:2] + MASK_STR + value[-2:]


def format_masked(prefix, value, suffix, extension):
    return (
        f"{prefix}'{value}'{suffix}"
        if extension == "yaml"
        else f'{prefix}"{value}"{suffix}'
    )


def partial_mask(value, extension):
    """
    Check length of the string. If it is too long, take 2 chars
    from beginning, then add mask string and add 2 chars from the
    end.
    If value is short, take just 2 chars and add mask string
    """
    if not value.strip():
        return
    if "'" in value or extension == "json":
        parsed_value = value.split('"') if extension == "json" else value.split("'")
        if len(parsed_value) > 2 and parsed_value[1] != "":
            prefix = parsed_value[0]
            value = _get_masked_string(parsed_value[1])
            suffix = parsed_value[2]
            return format_masked(prefix, value, suffix, extension)
    else:
        match = re.match(r"^(\s*)(.*?)(\n?)$", value)
        if match:
            parts = list(match.groups())
            prefix = parts[0]
            value = _get_masked_string(parts[1])
            suffix = parts[2]
            return format_masked(prefix, value, suffix, extension)


def mask(module, path: str) -> bool:
    """
    Function responsible to begin masking on a provided
    log file. It checks for file type, and calls
    respective masking methods for that file.
    """
    changed = False
    if path.endswith("json"):
        changed = mask_file(module, path, "json")
    elif (
        path.endswith((tuple(["yaml", "yml"])))
        or os.path.basename(path).split(".")[0] in ALLOWED_YAML_FILES
    ):
        changed = mask_file(module, path, "yaml")
    else:
        changed = mask_file(module, path, "log")
    return changed


def mask_log_line(line: str) -> str:
    """
    Masks several secrets occurrence in a single line.
    Works good with big file with long lines and sparse secrets.

    Returns masked line with secrets replaced by MASK_STR
    """

    line_lower = line.lower()
    has_keyword = any(kw in line_lower for kw in QUICK_KEYWORDS)

    if not has_keyword:
        return line

    # Python dict with quoted keys and quoted values
    # 'password': 'value' -> 'password': '**********'
    line = LOG_PATTERNS["python_dict_quoted"].sub(
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}: {m.group(4)}{MASK_STR}{m.group(6)}",
        line,
    )

    # Python dict with quoted keys and numeric values
    # 'password': 123456789 -> 'password': **********
    line = LOG_PATTERNS["python_dict_numeric"].sub(
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}: {MASK_STR}", line
    )

    # Plain KEY:VALUE or KEY=VALUE
    # password: value -> password: **********
    # token=abc123 -> token=**********
    line = LOG_PATTERNS["plain_key_value"].sub(
        lambda m: (
            f"{m.group(1)}={MASK_STR}"
            if "=" in m.group(0)
            else f"{m.group(1)}: {MASK_STR}"
        ),
        line,
    )
    # SHA256 tokens
    # sha256~abc123... -> sha256~**********
    line = LOG_PATTERNS["sha256_token"].sub(f"sha256~{MASK_STR}", line)

    # Bearer tokens
    # Bearer abc123... -> Bearer **********
    line = LOG_PATTERNS["bearer"].sub(f"Bearer {MASK_STR}", line)

    # connection_string tokens
    # Bearer abc123... -> Bearer **********
    line = LOG_PATTERNS["connection_string"].sub(f"://{MASK_STR}:{MASK_STR}@", line)

    return line


def should_skip_ansible_line(line: str) -> bool:
    """
    Identifies if the line is in an Ansible header for Tasks or Plays.

    Returns True for lines that should not be masked.
    """
    line_upper = line.upper()
    return any(pattern.upper() in line_upper for pattern in ANSIBLE_SKIP_PATTERNS)


def mask_log_file_lines(infile, outfile, changed) -> bool:
    """
    Mask log file lines with skip logic.

    """
    for line in infile:
        # Skip Ansible task headers - don't mask these
        if should_skip_ansible_line(line):
            outfile.write(line)
            continue

        masked_line = mask_log_line(line)
        if masked_line != line:
            changed = True
        outfile.write(masked_line)

    return changed


def mask_yaml_json_lines(infile, outfile, changed, extension) -> bool:
    """
    Read the file, search for colon (':'), take value and
    mask sensitive data
    """
    for line in infile:
        # Skip lines without colon
        if ":" not in line:
            outfile.write(line)
            continue

        key, sep, value = line.partition(":")
        comparable_key = key.strip().replace('"', "")
        masked_value = value

        for word in PROTECT_KEYS:
            if comparable_key == word.strip():
                masked = partial_mask(value, extension)
                if not masked:
                    continue
                masked_value = masked_value.replace(value, masked)
                changed = True

        outfile.write(f"{key}{sep}{masked_value}")

    return changed


def mask_by_extension(infile, outfile, changed, extension) -> bool:
    """
    Based on extension argument, calls the proper method for masking the file
    """
    if extension == "log":
        return mask_log_file_lines(infile, outfile, changed)
    return mask_yaml_json_lines(infile, outfile, changed, extension)


def replace_file(temp_path, file_path, changed):
    if changed:
        temp_path.replace(file_path)
    else:
        temp_path.unlink(missing_ok=True)


def mask_file(module, path, extension) -> bool:
    """
    Create temporary file, replace sensitive string with masked,
    then replace the tmp file with original.
    Unlink temp file when failure.
    """

    changed = False
    file_path = pathlib.Path(path)
    temp_path = file_path.with_suffix(".tmp")
    try:
        with file_path.open("r", encoding="utf-8") as infile:
            with temp_path.open("w", encoding="utf-8") as outfile:
                changed = mask_by_extension(infile, outfile, changed, extension)
        replace_file(temp_path, file_path, changed)
        return changed
    except Exception as e:
        print(f"An unexpected error occurred on masking file {file_path}: {e}")
        temp_path.unlink(missing_ok=True)
        module.fail_json(msg=f"Failed to mask {file_path}: {e}")
        return False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type="path", required=True), isdir=dict(type="bool", default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    changed = False
    result = dict(changed=changed)

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    params = module.params
    path = params["path"]
    isdir = params["isdir"]

    # validate if the path exists and no wrong value of isdir and path is
    # provided
    if not os.path.exists(path):
        module.fail_json(msg="Provided path doesn't exist", path=path)
    if os.path.isdir(path) != isdir:
        module.fail_json(msg="Value of isdir/path is incorrect. Please check it")

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if isdir:
        # craw through the provided directly and then
        # process eligible files individually
        changed = crawl(module, path)

    if not isdir and not re.search(excluded_file_ext_regex, path):
        changed = mask(module, path)

    result.update(changed=changed)
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
