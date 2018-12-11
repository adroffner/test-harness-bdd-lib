from unittest import TestCase, mock

import os.path
import sys

from testharness.bdd.compiler import testcase_writer

# Feature File: tests/features/TC-T1.feature
TC_T1_TEST_CASE = """
import unittest

from morelia import run


class FeatureTestCase(unittest.TestCase):

    FEATURE_FILE = 'tests/features/TC-T1.feature'

    def test_scenario_TC_T1(self):
        "BDD Scenario(s): tests/features/TC-T1.feature"
        run(self.FEATURE_FILE, self, verbose=True)

    def step_User_GETs_endpoint_relative_url(self, relative_url):
        r'User GETs endpoint (.+)'

        raise NotImplementedError('User GETs endpoint <relative_url>')

    def step_the_response_code_is_status_code(self, status_code):
        r'the response code is (.+)'

        raise NotImplementedError('the response code is <status_code>')

    def step_the_response_content_type_is_content_type(self, content_type):
        r'the response content-type is (.+)'

        raise NotImplementedError('the response content-type is <content_type>')

    def step_the_response_JSON_has_fields_field_list(self, field_list):
        r'the response JSON has fields (.+)'

        raise NotImplementedError('the response JSON has fields <field_list>')"""


class CompilerFunctionsTests(TestCase):

    def test_get_scenario_id(self):
        data = [
            # (expected_scenario_id, feature_filename)
            ('Test_Scenario', 'Test-Scenario.feature'),
            ('a100_Authentic', '100%~Authentic.feature'),  # invalid - starts with a digit
        ]

        for expected_result, feature_filename in data:
            result = testcase_writer.get_scenario_id(feature_filename)
            self.assertEqual(result, expected_result)

    def test_get_bdd_module_name(self):
        data = [
            # (expected_result, feature_filename) or ...
            # (scenario_id, bdd_filename), feature_filename),
            (('TC_T1', 'fake_TC_T1_feature.py'), 'tests/features/TC-T1.feature'),
        ]

        for expected_result, feature_file in data:
            result = testcase_writer.get_bdd_module_name('fake', feature_file)
            self.assertEqual(result, expected_result)


class CompilerTestCaseWriterTests(TestCase):

    def test_bdd_test_case_writer(self):
        # Real input file.
        testcase_writer.BDDTestCaseWriter.FEATURE_FILE = 'tests/features/TC-T1.feature'

        mock_testing_file = mock.mock_open()
        with mock.patch('testharness.bdd.compiler.testcase_writer.open',
                        mock_testing_file) as mock_file:
            writer = testcase_writer.BDDTestCaseWriter()
            (scenario_id, fake_file_path) = testcase_writer.get_bdd_module_name(
                writer.TESTING_PREFIX, writer.FEATURE_FILE)

            # Mocked output file must not exist to compile a new one.
            self.assertFalse(os.path.isfile(fake_file_path),
                             'Delete compiled file "{}" that interferes with tests.'.format(
                                 fake_file_path))

            writer.bdd_morelia_write_code()

            mock_file.assert_called_once_with(fake_file_path, 'w')
            self.assertEqual(mock_file().write.mock_calls, [
                mock.call('# Feature File: {}'.format(writer.FEATURE_FILE)),
                mock.call('\n'),   # print(..., file=f) adds newline after plain write().
                mock.call(TC_T1_TEST_CASE),
                mock.call('\n'),
            ])

    def test_bdd_test_case_writer_run_other_assertion_error(self):
        # Real input file.
        testcase_writer.BDDTestCaseWriter.FEATURE_FILE = 'tests/features/TC-T2.feature'

        with self.assertRaisesRegex(AssertionError, r'^BDD run'):

            # Mock morelia.run() to raise an uncaught exception.
            with mock.patch('testharness.bdd.compiler.testcase_writer.run',
                            side_effect=AssertionError('BDD run() failed!')):
                writer = testcase_writer.BDDTestCaseWriter()
                writer.bdd_morelia_write_code()

    def test_compile_function(self):
        feature_file = 'tests/features/TC-T2.feature'
        testing_prefix = 'test'

        # expected_bdd_filename = 'test_TC_T2_feature.py'

        with mock.patch('testharness.bdd.compiler.testcase_writer.os.path.isfile',
                        return_value=False):
            with mock.patch('testharness.bdd.compiler.testcase_writer.open',
                            mock.mock_open()) as mock_bdd_file:
                with mock.patch('testharness.bdd.compiler.testcase_writer.print',
                                return_value=None) as mock_print:
                    result = testcase_writer.compile(feature_file, testing_prefix)

                    self.assertTrue(result)
                    self.assertEqual(mock_print.mock_calls[0:2], [
                        mock.call('Compiling Feature: {}...\n\n'.format(
                            testcase_writer.BDDTestCaseWriter.FEATURE_FILE), file=sys.stderr),
                        mock.call('# Feature File: tests/features/TC-T2.feature', file=mock_bdd_file()),
                    ])

    def test_compile_function_bdd_module_exists(self):
        feature_file = 'tests/features/TC-T2.feature'
        testing_prefix = 'test'
        expected_bdd_filename = 'test_TC_T2_feature.py'

        with mock.patch('testharness.bdd.compiler.testcase_writer.os.path.isfile',
                        return_value=True):
            with mock.patch('testharness.bdd.compiler.testcase_writer.print',
                            return_value=None) as mock_print:
                result = testcase_writer.compile(feature_file, testing_prefix)

                # Compiler halts when the module file already exists.
                self.assertFalse(result)
                mock_print.assert_called_once_with(
                    'Cannot compile new feature file, "{}" already exists.\n'.format(
                        expected_bdd_filename), file=sys.stderr)
