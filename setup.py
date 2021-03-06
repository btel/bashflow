#!/usr/bin/env python
#coding=utf-8

from setuptools import setup

setup(name='bashflow',
      version='0.12',
      description='Bash-based workflow control',
      author='Bartosz Telenczuk',
      author_email='muchatel@poczta.fm',
      url='https://www.github.com/btel/bashflow',
      packages=['bashflow'],
      entry_points={
          'console_scripts': [
              'bashflow = bashflow.shell:run_shell',
          ],
      },
     )
