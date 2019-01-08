#! /bin/bash
#
# Unit Test Runner
# ======================================================
# Unit Tests are files like "test_*.py" (the default)
# ======================================================
 
# NOTE: Find reports dir.
REPORTS_DIR=$PWD
 
nosetests -v --testmatch='test_.*' \
    --with-xunit \
    --xunit-file="${REPORTS_DIR}/unittest.xml"
