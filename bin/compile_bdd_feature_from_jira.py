#! /usr/bin/env python
""" Compile BDD Test Cases from JIRA TM4J Folder

Test Management for JIRA stores BDD Test Cases in folders.
The TM4J REST API downloads any Gherkin feature files in a chosen folder.

BDD-Morelia compiles the un-implemented test steps from a Feature.
This script creates a directory of python test modules for them.
"""

import argparse
# import logging
import os
import pathlib
from getpass import getpass
from pprint import pprint

from jira_rest_clients.tm4j import JiraTM4JClient

from testharness.bdd.compiler import testcase_writer
from testharness.bdd.compiler.testcase_writer import PY_NAME_OK_RE
from testharness.bdd.tm4j.utils import create_bdd_feature_file


def _test_cases_folder2py_package(test_cases_folder, output_dir='.'):
    """ Turn Test Cases Folder into Python Package.

    Create python package directory under `output_dir`.
        test_cases_folder := "/SubProject/STORY-001"
        py_package        := ./output_dir/SubProject/STORY-001/__init__.py
        Feaure Files      := ./output_dir/SubProject/STORY-001/*.feature

    :param test_cases_folder: Test Cases folder like "/SubProject/STORY-001" in JIRA
    :param output_dir: existing output directory or '.'
    :returns: py_package_path a pathlib.Path object to the new directory.
    """

    output_path = pathlib.Path(output_dir)
    if not (output_path.exists() and output_path.is_dir()):
        raise ValueError('Missing or invalid output_path={}'.format(output_path))

    # Convert test_cases_folder path into valid python package dirs.
    test_cases_folder = os.path.join(*[
        PY_NAME_OK_RE.sub('_', p)
        for p in test_cases_folder.split(os.sep)])

    py_package_path = output_path / test_cases_folder.strip('/')
    if not (py_package_path.exists() and py_package_path.is_dir()):
        py_package_path.mkdir(parents=True)

        init_file = py_package_path / '__init__.py'
        init_file.touch()

    return py_package_path


def get_and_compile(test_cases_folder, testing_prefix, output_dir='.', verbose=False):
    jira_username = input('Enter JIRA Account ATTUID: ')
    jira_password = getpass('Enter JIRA Password: ')

    with JiraTM4JClient(jira_username, jira_password) as jira_client:
        test_case_results = jira_client.search_test_cases(
            'folder = "{}"'.format(test_cases_folder),
            fields=['testScript', 'key', 'folder'])

        if test_case_results:
            test_cases_package = _test_cases_folder2py_package(test_cases_folder, output_dir)

            for test_case_json in test_case_results:
                if verbose:
                    pprint(test_case_json, indent=4)
                feature_file = create_bdd_feature_file(test_case_json, test_cases_package)
                if feature_file:
                    testcase_writer.compile(os.path.join(test_cases_package, feature_file),
                                            testing_prefix, test_cases_package)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compile BDD Test Cases from JIRA TM4J Folder")

    parser.add_argument("test_cases_folder",
                        help='The JIRA Test Cases folder, e.g. "/Subproject/STORY-001"')
    parser.add_argument("-p", "--testing_prefix",
                        metavar='"test_stage"',
                        choices=['test', 'qa'],
                        default="test",
                        help='Set Testing Stage Prefix, e.g. "qa" Quality Assurance')
    parser.add_argument("-d", "--output_dir", default='.', metavar='<output-dir>',
                        help="A path to the output directory")
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Show info about each Test Case ticket.')

    args = parser.parse_args()

    get_and_compile(args.test_cases_folder, args.testing_prefix,
                    output_dir=args.output_dir, verbose=args.verbose)
