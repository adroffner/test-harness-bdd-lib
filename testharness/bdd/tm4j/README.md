Test Management for JIRA
========================

**Test Management for JIRA (TM4J)** is a plugin to write **test cases** and associate them
with a ticket, a **story** or **bug**. Python must download the **test plans** from JIRA.

TM4J REST API
-------------

These notes describe the REST API. Python interacts with **JIRA** over REST to execute **test plans**.

* (TM4J REST API Docs)[https://kanoah.com/docs/public-api/1.0/]

Status and Environment Fields
-----------------------------

Some entities, such as the Test Results, may have status and environment fields.
The values of these fields are identified by name below.

These **Status and Environment** fields may be mapped to the **XUnit** report format.
Test run reports generated in **XUnit XML** should be translated to **TM4J Test Run** JSON.

### Test Cases

**Test Case Status** determines what is ready to run. The REST API can filter on **status**.

| TM4J         | Description                     |
| ------------ | ------------------------------- |
| Draft        | Not ready to run, skip it       |
| Approved     | Ready to run                    |
| Deprecated   | Cancelled test                  |

### Test Runs

Translate **XUnit XML** reports to **TM4J status** codes.

* **testsuite** attributes tests="3" errors="0" failures="1" skip="0"

| TM4J         | XUnit     | Description                     |
| ------------ | --------- | ------------------------------- |
| Not Executed | skip=S    | Deliberately skipped test cases |
| In Progress  | (running) | Test suite is still running     |
| Done         | tests=T   | Total test cases, "tests"       |

### Test Results

Translate **XUnit XML** reports to **TM4J status** codes.

| TM4J         | XUnit                              | Description                     |
| ------------ | ---------------------------------- | ------------------------------- |
| Not Executed | skip=S                             | Deliberately skipped test cases |
| In Progress  | (running)                          | Test suite is still running     |
| Pass         | tests - (errors + failures + skip) | Compute passed tests            |
| Fail         | failures=F                         | Failed tests                    |
| Blocked      | errors=E                           | Run time errors blocked tests   |

REST API Examples
-----------------

We have the TM4J REST API at "/rest/atm/1.0/<object>" on our JIRA server.

* (Search for Project Tickets starting with "TC")[https://jira.web.att.com:8443/rest/atm/1.0/testcase/search?query=projectKey+%3D+%22TC%22]
* (Download All BDD Features for projectKey)[https://jira.web.att.com:8443/rest/atm/1.0/automation/testcases?query=projectKey+%3D+%22TC%22]
