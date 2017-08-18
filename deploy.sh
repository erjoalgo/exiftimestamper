#!/bin/bash -x

sudo rm -rf build  dist *.egg-info
python setup.py sdist
VERSION=${1:-$(cat VERSION | head -1 | tr -d '\n')}
PROJECT_NAME=$(basename $(pwd))
TARGZ=dist/${PROJECT_NAME}-${VERSION}.tar.gz
test -e ${TARGZ} || exit ${LINENO}
gpg --detach-sign -a ${TARGZ} || exit ${LINENO}
gpg --verify -a ${TARGZ}{.asc,} || exit ${LINENO}

if ! command -v twine; then
    pip install --user twine
fi

CMD=$(echo twine upload ${TARGZ}{,.asc})
read -p "${CMD} :"
${CMD}
