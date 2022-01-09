BDD Gherkin Test Harness for Python unittest
============================================

BDD [behavior driven development](https://en.wikipedia.org/wiki/Behavior-driven_development) provides 
a way to plan **unit tests** or **integration tests** as a team. A common **behavior outline** is shared
between the business, data or test analyst and the programmers.

Python and Automated Testing
----------------------------

The **behavior outline** is compiled to a **test harness** and automates **Python BDD Testing**.
The tests rely on a prepared **Gherkin Feature file** to provide the testing **scenario's _steps_**.
Each **behavior outline** is a formal **Gherkin Feature file** with a _.feature_ suffix.

Testing Stages
--------------

This library supports multiple *testing stages*, depending on which **unittest.TestCase** subclass is used.

* **Unit Testing with Mock Services**: The tests do not interact with live services.
* **QA or Regression Testing**: The tests interact with live, fully installed services.

[BDD Python with morelia](https://morelia.readthedocs.io/en/latest/)
-----------------------

The *Test Analyst* shall write **Gherkin Feature files** as input compatible
with the [Morelia Gherkin Syntax dialect](https://morelia.readthedocs.io/en/latest/gherkin.html).
This project compiles the *.feature* file into python3 **unittest.TestCase** _steps_.

[Cucumber Gherkin Syntax](https://cucumber.io/docs/gherkin/reference/)
-----------------------

The **Cucumber Gherkin Syntax** is the _de facto_ BDD Test specification format.
Each **Feature file** has one _or more_ **scenario outlines** to describe _step by step_ usages.

* [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/reference/)
* [Writing Gherkin Scenarios](https://support.smartbear.com/cucumberstudio/docs/bdd/write-gherkin-scenarios.html)