#!/bin/bash

# Validate that each commit in the PR has the correct role prefix
# based on the roles modified in that specific commit.

if [ -z "$GITHUB_BASE_REF" ]; then
    echo "Not running in GitHub Actions - skipping check"
    exit 0
fi

echo "Checking all commits in PR against base: origin/${GITHUB_BASE_REF}"
echo ""

# Get all commits in the PR
commits=$(git rev-list origin/${GITHUB_BASE_REF}..HEAD)

if [ -z "$commits" ]; then
    echo "No commits to check"
    exit 0
fi

failed=0

# Check each commit individually
while IFS= read -r commit; do
    msg=$(git log -1 --pretty=format:"%s" "$commit")
    echo "Checking commit ${commit:0:8}: $msg"

    # Get roles changed in THIS commit only
    changed_roles=$(git diff-tree --no-commit-id --name-only -r "$commit" | grep '^roles/' | cut -d'/' -f2 | sort -u | xargs | sed 's/ /|/g')

    if [ -z "$changed_roles" ]; then
        echo "  No roles modified - skipping"
        echo ""
        continue
    fi

    echo "  Changed roles: $changed_roles"

    role_count=$(echo "$changed_roles" | tr '|' '\n' | wc -l)

    if [ "$role_count" -eq 1 ]; then
        # shellcheck disable=SC2016
        escaped_role=$(printf '%s\n' "$changed_roles" | sed 's/[]\.*^$()+?{|]/\\&/g')
        pattern="^[[(]${escaped_role}[])]"
    else
        pattern="^[[(](multiple)[])]"
    fi

    if ! grep -qE "$pattern" <<<"$msg"; then
        echo ""
        echo "  **ERROR: Commit message must start with:**"
        if [ "$role_count" -eq 1 ]; then
            echo "    [$changed_roles]"
        else
            echo "    (multiple)"
        fi
        echo ""
        failed=1
    else
        echo "  ✓ Valid prefix"
    fi
    echo ""
done <<< "$commits"

if [ $failed -eq 1 ]; then
    echo "Example commit messages:"
    echo "  [reproducer] fix task something"
    echo "  (multiple) updated default value"
    exit 1
fi

echo "Each commit message prefix is valid."
