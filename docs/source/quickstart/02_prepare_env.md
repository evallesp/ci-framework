# Prepare your environment

## Tested environment

The following operating systems were successfully tested:

- Fedora Core 38, 39 (for laptop/desktop)
- CentOS Stream 9 (for the hypervisor, laptop/desktop)
- Red Hat Enterprise Linux 9.3 (for the hypervisor, laptop/desktop)

## On your laptop/desktop

There are a few needed dependencies to install before starting consuming the framework:

```Bash
[laptop]$ sudo dnf install -y git-core make
[laptop]$ git clone https://github.com/openstack-k8s-operators/ci-framework ci-framework
[laptop]$ cd ci-framework
[laptop]$ make setup_molecule
[laptop]$ source ~/test-python/bin/activate
```

## On the hypervisor

On the hypervisor, please ensure you have:

- a non-root user, with passwordless SSH access (use SSH keys)
- `sudo` configuration allowing that non-root user to run any random command, with or without password
- at least 400G of free space in /home
- an up-to-date CentOS Stream 9 or RHEL-9.3 system

Note: if you chose to require a password for `sudo`, please ensure to pass the `-K` option to any
`ansible-playbook` command running against the hypervisor.

## Bootstrap hypervisor

Since we're using non-root user with some specificities, you may want to get an automated way to provision the
hypervisor.

### Basics

The boostrap-hypervisor.yml will help you create the user, ensuring some
packages are present, as well as ensuring your user will be part of the needed group.

You can run the playbook like this:

```Bash
$ cd ci-framework
$ ansible-playbook -i custom/inventory.yml \
    -e ansible_user=root \
    -e cifmw_target_host=[hypervisor|hypervisors] \
    docs/source/files/bootstrap-hypervisor.yml
