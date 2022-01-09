import unittest
from unittest import TestCase

import os.path

from testharness.bdd.tm4j import report_testruns

XUNIT_SAMPLES_DIR = 'tests/testharness/bdd/tm4j/xunit_samples'  # '/prove_script_results.xml'

EXPECTED_STATUSES = [
    'Blocked',  # ERROR occurred
    'Fail',
    'Not Executed',
    'Pass'
]

EXPECTED_STATUS_ALL = [
    # Counters: Each status takes precedence over the one to the right.
    # (('Blocked', 'Fail', 'Pass' 'Not Executed'), expected_status_all)
    ((0, 0, 0, 4), 'Not Executed'),  # Not one test executed and got a status
    ((2, 0, 2, 0), 'Blocked'),       # ERROR: At least one was blocked
    ((1, 1, 1, 1), 'Blocked'),
    ((0, 2, 2, 0), 'Fail'),          # At least one failed, but there were no errors
    ((0, 2, 1, 1), 'Fail'),
    ((0, 0, 3, 1), 'Pass'),          # Everything either passed or was never executed
    ((0, 0, 4, 0), 'Pass'),
]


@unittest.skip('Removing JIRA TM4J')
class SuiteStatusCounterTests(TestCase):

    def setUp(self):
        self.machine = report_testruns.SuiteStatusCounter()

    def test_counters_ready(self):
        """Prove counters handle all statuses starting at zero"""

        for status in EXPECTED_STATUSES:
            self.assertIn(status, self.machine.counters)
            self.assertEqual(self.machine.counters[status], 0)

    def test_counters_tally(self):
        """Prove each counter can add +1 to status tally"""

        for status in EXPECTED_STATUSES:
            self.assertEqual(self.machine.counters[status], 0)
            self.machine.tally(status)
            self.assertEqual(self.machine.counters[status], 1)

    def test_status_all(self):
        for counters_set, expected_status_all in EXPECTED_STATUS_ALL:
            # Set counters to counters_set values.
            self.machine.counters = {
                'Blocked': counters_set[0],
                'Fail': counters_set[1],
                'Pass': counters_set[2],
                'Not Executed': counters_set[3]
            }
            self.assertEqual(self.machine.status_all, expected_status_all)


# ====================================================================

EXPECTED_TESTSUITE_NAME = 'Example REST API Suite'
EXPECTED_PROJECT_KEY = 'TC'

EXPECTED_TESTCASE_KEY = 'TC-T1'
EXPECTED_USER_KEY = 'username'
EXPECTED_COMMENT = 'This is only a test. If it had been an actual emergency...'
EXPECTED_ENVIRONMENT = 'REST API'

EXPECTED_TESTRUN_RESULTS = [
    {
        'name': EXPECTED_TESTSUITE_NAME,
        'projectKey': EXPECTED_PROJECT_KEY,
        'status': 'Done',  # always "Done"
        # 'testPlanKey': 'TC-P1'  # Are Test Plans required?
        'items': [
            {
                'testCaseKey': EXPECTED_TESTCASE_KEY,
                'status': 'Blocked',
                'userKey': EXPECTED_USER_KEY,
                'comment': EXPECTED_COMMENT,
                'environment': EXPECTED_ENVIRONMENT,
                'executionDate': '2018-11-23T19:13:43',
                'executionTime': 0.847,
                'scriptResults': [
                    {
                        'comment': 'test_zero_TC_T1',
                        'index': 0,
                        'status': 'Pass'
                    },
                    {
                        'comment': 'test_one_TC_T1',
                        'index': 1,
                        'status': 'Blocked'
                    },
                    {
                        'comment': 'test_two_TC_T1',
                        'index': 2,
                        'status': 'Not Executed'
                    },
                    {
                        'comment': 'test_three_TC_T1',
                        'index': 3,
                        'status': 'Fail'
                    },
                    {
                        'comment': 'test_four_TC_T1',
                        'index': 4,
                        'status': 'Pass'
                    }
                ]
            }
        ]
    }
]


@unittest.skip('Removing JIRA TM4J')
class TM4JTestRunReporterTests(TestCase):

    maxDiff = None

    def test_reporter_and_xunit_file(self):
        xunit_file = os.path.join(XUNIT_SAMPLES_DIR, 'prove_script_results.xml')
        reporter = report_testruns.TM4JTestRunReporter(xunit_file, EXPECTED_USER_KEY,
                                                       comment=EXPECTED_COMMENT,
                                                       environment=EXPECTED_ENVIRONMENT)
        results = reporter.all_testrun_reports

        self.assertEqual(results, EXPECTED_TESTRUN_RESULTS)
