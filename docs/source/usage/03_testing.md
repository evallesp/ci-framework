# Testing

Right now we are using 3 different CI systems in the CI Framework project:

- Github workflows
- Zuul CI
- Prow CI

The goal was to unify the tests in a single CI system but since we can't have privilege escalation using Prow CI, the team has decided to use Zuul CI to execute tests under each ansible role.

## Github workflow
A series of Github workflows take place in the pull request checks:

- Spellchecking using pySpelling
- Ensure commit message has a (checked) checklist
- CodeQL (actually a scheduled run)

### Spellchecking
We're using pySpelling, a python wrapper around aspell. You can add custom words
in the `docs/dictionary/en-custom.txt` file. In order to keep it tidy and
avoid duplication, please do as follow:
```Bash
[laptop]$ sudo dnf install -y aspell-en
[laptop]$ pip install pyspelling
[laptop]$ make spelling
# Correct actual spelling issues, or add new words to
# docs/dictionary/tmp
# Then, validate again the spelling (and re-build the dictionary)
[laptop]$ make spelling
```
That way, you ensure that only unique, lower-case words are added to the list.
