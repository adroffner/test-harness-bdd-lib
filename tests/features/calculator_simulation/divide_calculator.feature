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