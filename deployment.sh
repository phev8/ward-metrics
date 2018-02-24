#!/usr/bin/env bash

python3 setup.py bdist_wheel --universal

twine upload dist/*