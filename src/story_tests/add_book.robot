*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Book Page

*** Test Cases ***
Add Book With Valid Information And Only Required Fields Filled
    Set Title  A Brief History of Time: From the Big Bang to Black Holes 
    Set Author  Stephen Hawking
    Set Year    1988
    Submit Book
    Page Should Contain  Book added successfully!

Add Book With Too Short Title
    Set Title   T
    Set Author  Matti Meikalainen
    Set Year  1999 
    Submit Book
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Book With Required Fields Not Filled
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Book
    Page Should Not Contain  Book added successfully!

Add Book With Invalid Year
    Set Title  A Brief History of Time: From the Big Bang to Black Holes 
    Set Author  Stephen Hawking
    Set Year    2288
    Submit Book
    Page Should Not Contain  Book added successfully!

Add Book With All Fields Filled
    Set Title  Artificial Intelligence: A Modern Approach
    Set Author  Stuart J. Russell and Peter Norvig
    Set Year    2010
    Set Publisher  Prentice Hall
    Set Edition  3
    Set Pages  20-28
    Set Doi  10.5555/1214993
    Submit Book
    Page Should Contain  Book added successfully!


*** Keywords ***
Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Author 
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Year 
    [Arguments]  ${year}
    Input Text  year  ${year}

Set Publisher 
    [Arguments]  ${publisher}
    Input Text  publisher  ${publisher}

Set Edition 
    [Arguments]  ${edition}
    Input Text  edition  ${edition}

Set Pages 
    [Arguments]  ${pages}
    Input Text  pages  ${pages}

Set Doi 
    [Arguments]  ${doi}
    Input Text  doi  ${doi}

Submit Book
    Scroll Element Into view  submit
    Click Button  submit
