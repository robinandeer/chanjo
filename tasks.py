#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from invoke import run, task
from invoke.util import log


@task
def test():
  """Run the test runner."""
  run('python setup.py test', pty=True)


@task
def clean():
  """clean - remove build artifacts."""
  run('rm -rf build/')
  run('rm -rf dist/')
  run('rm -rf chanjo.egg-info')
  run('find . -name __pycache__ -delete')
  run('find . -name *.pyc -delete')
  run('find . -name *.pyo -delete')
  run('find . -name *~ -delete')
  log.info('cleaned up')


@task(clean)
def publish(test=False):
  """Publish to the cheeseshop."""
  if test:
    run('python setup.py register -r test sdist upload -r test')
  else:
    run('python setup.py register bdist_wheel upload')
    run('python setup.py register sdist upload')
  log.info('published new release')


@task
def coverage():
  """Run test coverage check and open HTML report."""
  run('coverage run --source chanjo setup.py test')
  run('coverage report -m')
  run('coverage html')
  run('open htmlcov/index.html')
  log.info('collected test coverage stats')