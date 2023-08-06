#!/usr/bin/env python3

from distutils.core import setup

long_desc = 'Licensed under the generic MIT License. nimbus-pod can either be downloaded from the ' \
            'Releases page on GitHub and manually added to PATH or installed via pip.'
version = ''

with open("version.txt", "r", encoding="utf-8") as fh:
    version = fh.read()
    fh.close()

setup(name='nimbus-pod',
      version=version,
      py_modules=['main'],
      description='Nimbus Pod | FastAPI System Service',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author='Tushar Iyer',
      author_email='',
      url='https://github.com/iyer-cloud/nimbus-pod',
      project_urls={
              "Bug Tracker": "https://github.com/iyer-cloud/nimbus-pod/issues",
          }
      )