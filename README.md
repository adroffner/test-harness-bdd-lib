BDD Gherkin Test Harness for Python unittest
============================================

* [Python and Automated Testing](https://wiki.web.att.com/display/GCSDevOps/Python+and+Automated+Testing)

This **test harness** automates **BDD Testing with JIRA TM4J**.
The tests rely on a prepared **Gherkin Feature file** to provide the scenario **steps**.

Testing Stages
--------------

This library supports multiple *testing stages*, depending on which **unittest.TestCase** subclass is used.

* **Unit Testing with Mock Services**: The tests do not interact with live services.
* **QA or Regression Testing**: The tests interact with live, fully installed services.

BDD Python with morelia
-----------------------

* [Morelia BDD Library](https://morelia.readthedocs.io/en/latest/)

The *Test Analyst* must learn to write **Gherkin Feature files** as input.
Then, learn to compile the *.feature* file into python3 **unittest.TestCase** _steps_.
