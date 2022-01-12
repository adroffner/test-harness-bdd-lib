Feature: Dividing numbers with a Calculator
  I want to be able to divide numbers using a Calculator

  Background:
    Given the Calculator is powered on

  Scenario Outline: Divide a positive number by another
    When I divide <numerator> by <denominator>
    Then the quotient should be <result>

      Examples:
              | numerator | denominator | result |
              |         1 |           1 |      1 |
              |         5 |           2 |    2.5 |

  Scenario: Division by zero raises an error
    Given the Calculator is not in the error state
    When I try to divide by zero
    Then the calculator goes to the value error state