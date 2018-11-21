BDD Feature Files: Example Data Files
=====================================

Some **BDD .feature** files have a **Scenario Outline** with _example data_.
However, the **Examples:** data table can only store small constant strings, numbers, etc.
Larger data must be kept in auxiliary _data files_.

Directory: features/data
------------------------

This directory maps _data files_ by name to **data table cells**.
When a **BDD step** visits a **Scenario Outline** parameter,
the python code may choose to load it as a _filename_, rather than a constant.

Example Data Files
------------------

Here are common reasons to use a _data file_ in a **data table cell**.

* A REST API **POST Payload**: Send the input payload **guestbook_signin.json**
* A REST API **Response Payload**: Read the **HTTP response**, **guestbook_response.json**
* A Spreadsheet **File Upload**: Open and send a known Excel file
