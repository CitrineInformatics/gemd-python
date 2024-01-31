#!/usr/bin/env bash

for i in "$@"; do
  case $i in
    -q|--quiet)
      QUIET="--quiet --no-cov-on-fail "
      shift # past argument=value
      ;;
    -x|--exitfirst)
      EXITFIRST="--exitfirst "
      shift # past argument=value
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      ;;
  esac
done

REPO_DIR=`git rev-parse --show-toplevel`

# following https://docs.travis-ci.com/user/environment-variables/#convenience-variables
# the pull request isn't set to true if its a PR; its just set to false if its not.
if [ -z "$TRAVIS_PULL_REQUEST" ];  # Not Travis context
then
    if [ "`git rev-parse --abbrev-ref HEAD`" == "main" ];
    then echo "On main branch";                                                  exit 1;
    else python $REPO_DIR/scripts/validate_version_bump.py                    || exit 1;
    fi
# only run the validate-version_bump.py script on PR builds against main,
# since those have access to a "main" reference to git show the version
elif [ "$TRAVIS_PULL_REQUEST" != "false" ] && [ "$TRAVIS_BRANCH" == "main" ];
then python $REPO_DIR/scripts/validate_version_bump.py                        || exit 1;
fi

flake8 $REPO_DIR/gemd                                                         || exit 1;
<<<<<<< HEAD
derp $REPO_DIR/gemd $REPO_DIR/setup.py                                        || exit 1;
=======
derp $REPO_DIR $REPO_DIR/gemd/__version__.py                                  || exit 1;
>>>>>>> main
pytest $QUIET $EXITFIRST --cov=$REPO_DIR/gemd                                \
       --cov-report term-missing:skip-covered                                \
       --cov-config=$REPO_DIR/tox.ini --no-cov-on-fail --cov-fail-under=100  \
       $REPO_DIR                                                              || exit 1;
