*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add DOI

*** Test Cases ***
Add Article With Valid DOI
    Set DOI  10.1177/1470593113512323
    Submit DOI
    Textfield Value Should Be  title    The brand personality of rocks: A critical evaluation of a brand personality scale
    Textfield Value Should Be  author    Avis, Mark and Forbes, Sarah and Ferguson, Shelagh
    Textfield Value Should Be    journal    Marketing Theory
    Textfield Value Should Be  year    2013
    Textfield Value Should Be  volume    14
    Textfield Value Should Be  number    4
    Textfield Value Should Be  pages    451–475
    Textfield Value Should Be  month    December
    Textfield Value Should Be  doi    10.1177/1470593113512323
    Submit Reference
    Page Should Contain  Article added successfully!

Add Book With Valid DOI
    Set DOI  10.1037/0000168-000
    Submit DOI
    Textfield Value Should Be  title    The psychology of prejudice: From attitudes to social action (2nd ed.).
    Textfield Value Should Be  author    Jackson, Lynne M.
    Textfield Value Should Be  year    2020
    Textfield Value Should Be  publisher    American Psychological Association
    Textfield Value Should Be  doi    10.1037/0000168-000
    Submit Reference
    Page Should Contain  Book added successfully!

Add Unsuccessful When DOI Is Non-existent
    Set DOI  10.1177/1470593113512324
    Submit DOI
    Page Should Contain  HTTP Error 404: Not Found

Add Unsuccessful When DOI Formt Is Invalid
    Set DOI  10.11
    Submit DOI
    Page Should Contain  DOI must follow the format '10.xxxx/xxxxx'.

*** Keywords ***
Set DOI
      [Arguments]  ${doi}
      Input Text  doi  ${doi}

Submit DOI
    Scroll Element Into view  submit
    Click Button  submit

Submit Reference
    Scroll Element Into view  submit
    Click Button  submit