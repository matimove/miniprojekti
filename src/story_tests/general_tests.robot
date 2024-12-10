*** Settings ***
Resource  resource.robot 
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Misc Page

*** Test Cases ***
Success Messages Close
    Go To Add Article Page
    Set Title  Adam: A method for stochastic optimization
    Set Author  Kingma, Diederik P and Ba, Jimmy
    Set Journal  arXiv preprint
    Set Year  2014
    Submit Article
    Page Should Contain  Article added successfully!
    Click Button  close_message

*** Keywords ***
Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Journal
    [Arguments]  ${journal}
    Input Text  journal  ${journal}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Submit Article
    Scroll Element Into view  submit
    Click Button  submit

