#! /usr/bin/env python
""" Compile BDD Test Case from Gherkin Feature File.

BDD-Morelia lists the un-implemented test steps from a Feature.
This script creates a full python test module for them.
"""
from getpass import getpass
import logging
import pathlib
import argparse
from jira_client.tm4j import JiraTM4JClient
from bdd.tm4j.utils import create_bdd_feature_file
from bdd.compiler.testcase_writer import PY_NAME_OK_RE
from pprint import pprint

# from bin.secrets import jira_username, jira_password
from testharness.bdd.compiler import testcase_writer


def _make_package_from_test_case_folder(folder_to_search_for, results_dir):
    feature_file_directory = folder_to_search_for.split('/')[-1]
    feature_file_directory = results_dir + '/' + PY_NAME_OK_RE.sub('_', feature_file_directory)

    p = pathlib.Path(feature_file_directory)

    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

        init_file = p / '__init__.py'
        init_file.touch()

    return feature_file_directory


def get_and_compile(folder_to_search_for, testing_prefix, results_dir='.'):
    jira_username = input('Enter JIRA Account ATTUID: ')
    jira_password = getpass('Enter JIRA Password: ')

    with JiraTM4JClient(jira_username, jira_password) as jira_client:
        test_case_results = jira_client.search_test_cases(
            'folder = "{}"'.format(folder_to_search_for),
            fields=['testScript', 'key', 'folder'])

    if test_case_results:
        feature_file_directory = _make_package_from_test_case_folder(folder_to_search_for, results_dir)

        for test_case_json in test_case_results:
            pprint(test_case_json, indent=4)
            try:
                feature_file = create_bdd_feature_file(test_case_json, feature_file_directory)
                if feature_file:
                    testcase_writer.compile(feature_file_directory + '/' + feature_file,
                                            testing_prefix,
                                            feature_file_directory)
            except Exception:
                logging.exception('Error with json: {}'.format(test_case_json))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compile BDD Test Case module from Feature Files found in JRIA Test Cases.")

    parser.add_argument("test_case_folder_search",
                        help="The JIRA Test Case folder to search for. EXAMPLE/TES-001")
    parser.add_argument("-p", "--testing_prefix",
                        metavar='"test_stage"',
                        choices=['test', 'qa'],
                        default="test",
                        help='Set Testing Stage Prefix, e.g. "qa" Quality Assurance')
    parser.add_argument("-d", "--results_dir", default='.', metavar='<path/to/dir>',
                        help="A path to the directory you want your results in")

    args = parser.parse_args()

    get_and_compile(args.test_case_folder_search, args.testing_prefix, args.results_dir)


