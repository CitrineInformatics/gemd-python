# Contributing

## Coding Style
This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/), with the following exceptions:
* Maximum line length is 99 characters

For additional (non-binding) inspiration, check out the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

## Branching strategy

This project currently follows a [feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) (i.e. _masterflow_):
 * Feature branches and bugfixes are branched off of master and then opened as PRs into master
 * Every PR must contain a version bump following [semantic versioning](https://semver.org/).
 * Backport branches for historical versions are created as-needed off of master; backports are branched off of and merged into them
 
 During periods of rapid development activity, the branching strategy may change to accomodate it, but it will be kept up to date here.

## Release process

The master branch **does not** continuously deploy to [pypi](https://pypi.org/project/gemd/).
Rather, releases are cut explicitly by using [Github's releases](https://github.com/CitrineInformatics/gemd-python/releases) and creating a tag that matches the version number of the commit being released.
Travis will trigger the deploy due to the addition of the tag.
Only commits on the **master** or backports branches can be released, but it need not be the most recent commit on the branch.
The tests contained within this repository are sufficient to verify a release.
 
