Feature: Dividing numbers with a Calculator
  I want to be able to divide numbers using a Calculator

  Background:
    Given the Calculator is powered on

  Scenario Outline: Divide a positive number by another
    When I divide <numerator> by <denominator>
    Then the answer should be <quotient>

      Examples:
              | numerator | denominator | quotient |
              |         1 |           1 |        1 |