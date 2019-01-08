#! /bin/bash
#
# QA Test Runner
# ======================================================
# Quality Assurance test are files like "qa_*.py"
# ======================================================
 
# NOTE: Find reports dir like the unit test suite does.
REPORTS_DIR=$PWD
 
nosetests -v --testmatch='qa_.*' \
    --with-xunit \
    --xunit-file="${REPORTS_DIR}/qalivetest.xml"
