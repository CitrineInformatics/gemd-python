# Contributing

## Testing

Changes are gated on:
 * Passing unit tests
 * 100% unit test coverage
 * PEP8 style compliance, with some exceptions in the [tox file](tox.ini)
 * Incrementing the package version number in [setup.py](setup.py)

Travis runs the tests in `scripts/run_tests.sh`, which gives a convenient one-line invocation for testing.

As it can be easy to forget to verify these prior to pushing, it's possible to use [git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to enforce compliance during normal workflows.
Consider editing `.git/hooks/pre-commit` or `.git/hooks/pre-push` (or adding them and marking them as executable: `chmod +x <file>`). 
For example, you could set your local `.git/hooks/pre-commit` to be
```shell
scripts/run_tests.sh --quiet --exitfirst
```
to make sure you're not on the `main` branch, you've incremented the package version, you pass the linter and you have complete, passing tests.

## Coding Style
This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/), with the following exception:
* Maximum line length is 99 characters

Additionally:
* Type hints are strongly encouraged, but not required.
* Positional arguments are strongly discouraged for methods with multiple arguments.  Keyword-only arguments are preferred instead.  Every positional argument should be required.

For additional (non-binding) inspiration, check out the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

## Branching strategy

This project currently follows a [feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow):
 * Feature branches and bugfixes are branched off of `main` and then opened as PRs into `main`
 * Every PR must contain a version bump following [semantic versioning](https://semver.org/)
 * Backport branches for historical versions are created as-needed off of `main`; backports are branched off of and merged into them
 
 During periods of rapid development activity, the branching strategy may change to accommodate it, but it will be kept up to date here.

## Release process

The `main` branch **does not** continuously deploy to [pypi](https://pypi.org/project/gemd/).
Rather, releases are cut explicitly by using [GitHub's releases](https://github.com/CitrineInformatics/gemd-python/releases).
To create a release:
 * Catalog the changes in order to inform release notes
   * To do this through the GitHub interface:
     * Navigate to the [GitHub compare page](https://github.com/CitrineInformatics/gemd-python/compare)
     * Set the `base` to the most recent tag (which corresponds to the most recent release)
     * Set the `compare` to the commit you want to deploy, typically `main`
   * You can use `git diff` as well, if you prefer
 * In another tab, navigate to the [GitHub release creation page](https://github.com/CitrineInformatics/gemd-python/releases/new)
 * Set the `Target` to the commit you want to deploy, typically `main`
 * Set the `Tag version` to `v{x.y.z}` where `x.y.z` is the version in [setup.py](setup.py), e.g. `v1.2.3`
 * Set the `Release title` to "GEMD v{x.y.z} is released!"
 * Populate the release notes with a 1 or 2 sentence summary and `What's New`, `Improvements`, `Fixes`, and `Deprecated` sections, as appropriate

Travis will trigger the deploy due to the addition of the tag.
Only commits on the **main** or backports branches can be released, but it need not be the most recent commit on the branch.
The tests contained within this repository are sufficient to verify a release. 
