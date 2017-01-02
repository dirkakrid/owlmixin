#!/usr/bin/env bash

python setup.py bdist_wheel
twine upload dist/owlmixin-${RELEASE_VERSION}-py2.py3-none-any.whl \
  --repository-url "https://pypi.python.org/pypi" \
  --config-file ".pypirc" \
  -u tadashi-aikawa \
  -p ${PYPI_PASSWORD}
