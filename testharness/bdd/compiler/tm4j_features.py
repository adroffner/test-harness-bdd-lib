""" Compile BDD Test Cases from JIRA TM4J Folder

Test Management for JIRA stores BDD Test Cases in folders.
The TM4J REST API downloads any Gherkin feature files
and example data into a target directory.

BDD-Morelia compiles the un-implemented test steps from a Feature.
This module creates or updaates a directory of python test modules for them.
"""

import os
import pathlib

from pprint import pformat

from jira_rest_clients.tm4j import JiraTM4JClient

from testharness.bdd.compiler import testcase_writer
from testharness.bdd.compiler.testcase_writer import PY_NAME_OK_RE
from testharness.bdd.tm4j.utils import create_bdd_feature_file

import logging
log = logging.getLogger(__name__)

TEST_CASES_JQL_FMT = 'projectKey = "{}" AND status = "Approved" AND folder = "{}"'


def _test_cases_folder2py_package(test_cases_folder, output_dir='.'):
    """ Turn Test Cases Folder into Python Package.

    Create python package directory structure under `output_dir`.
        test_cases_folder := "/SubProject/STORY-001"
        py_package        := ./output_dir/SubProject/__init__.py
                             ./output_dir/SubProject/STORY-001/__init__.py
        Feaure Files      := ./output_dir/SubProject/STORY-001/features/TEST-002.feature
        Data Files        := ./output_dir/SubProject/STORY-001/features/data/TEST-002/*.*

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

        # Write "__init__.py" in each python package directory.
        py_partial_path = output_path
        for p in test_cases_folder.split(os.sep):
            py_partial_path = py_partial_path / p

            init_file = py_partial_path / '__init__.py'
            init_file.touch()

        features_path = py_package_path / 'features' / 'data'
        features_path.mkdir(parents=True)

    return py_package_path


def get_tm4j_features(test_cases_folder, testing_prefix,
                      jira_username, jira_password,
                      project_key='MIC', output_dir='.',
                      compile_new_modules=False, verbose=False):
    """ Get TM4J Features.

    Get BDD "feature file" test scripts and example data from JIRA.
    The first time, `compile_new_modules` to make stub test modules from *.feature files.

    :param test_cases_folder: JIRA Test Cases folder, e.g. "/Subproject/STORY-001"
    :param testing_prefix: test stage prefix in ('test', 'qa')
    :param jira_username: JIRA REST (TM4J) account username
    :param jira_password: JIRA REST (TM4J) account password
    :param project_key: JIRA "project key", e.g. "MIC" (microservices) or "INC" (incubate)
    :param output_dir: optional target output must exist, default PWD
    :param compile_new_modules: Set to True to compile test_*.py from *.feature files
    :param verbose: a boolean flag to show the JIRA BDD query
    :raises: ValueError when test_cases_folder is no good
    """

    # Test Cases Folder must start with slash for TM4J.
    if not test_cases_folder.startswith('/'):
        test_cases_folder = '/' + test_cases_folder

    with JiraTM4JClient(jira_username, jira_password) as jira_client:
        test_case_results = jira_client.search_test_cases(
            TEST_CASES_JQL_FMT.format(project_key, test_cases_folder),
            fields=['testScript', 'key', 'folder'])

        if test_case_results:
            test_cases_package = _test_cases_folder2py_package(test_cases_folder, output_dir)

            # Download Feature files (and compile test modules when flag is True).
            for test_case_json in test_case_results:
                if verbose:
                    log.info(pformat(test_case_json, indent=4))
                feature_file = create_bdd_feature_file(test_case_json, test_cases_package / 'features')
                if feature_file and compile_new_modules:
                    testcase_writer.compile(os.path.join(test_cases_package, 'features', feature_file),
                                            testing_prefix, test_cases_package)

            # Download Feature "attachments" data files.
            features_dir = test_cases_package / 'features'
            for feature_file in features_dir.glob('*.feature'):
                data_dir = features_dir / 'data' / feature_file.stem
                if not (data_dir.exists() and data_dir.is_dir()):
                    data_dir.mkdir(parents=True)
                file_count = jira_client.download_test_case_attachments(feature_file.stem, data_dir)
                if verbose:
                    log.info('\tFeature "{}" has {} data files.'.format(feature_file.stem, file_count))

        else:
            raise ValueError('JIRA and TM4J have no "{}" BDD files'.format(test_cases_folder))
