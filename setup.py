#! /usr/bin/env python

from setuptools import setup, find_packages
from testharness.bdd import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='testharness_bdd',
      version=__version__,
      license='PSF',
      description='Behavior Driven Development (BDD) Test Harness for unittest',
      long_description=readme(),
      author='Andrew Droffner',
      author_email='ad718x@us.att.com',
      url='https://codecloud.web.att.com/projects/ST_TITAN/repos/test-harness-bdd-lib/browse',
      packages=find_packages(exclude=['docs', 'tests']),
      include_package_data=True,
      install_requires=[
          'jira_rest_clients>=0.1b1',
          'morelia>=0.6.5',
          'nose>=1.3.7'
      ],
      scripts=[
          'bin/compile_bdd_feature',
          'bin/compile_bdd_feature_from_jira',
          'bin/update_bdd_feature_from_jira',
      ],
      # NO nosetests: junitparser.TestSuite confuses nose, testing ERRORs
      # test_suite='nose.collector',
      # tests_require=['nose>=1.3.7', 'coverage>=4.4.1'],
      # NOTE: ./setup.py nosetests <= needs "setup_requires"
      setup_requires=[
          'coverage>=4.4.1'
      ],
      keywords=[
          'testharness', 'test', 'harness',
          'selenium',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
      ])
