*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Book Page

*** Test Cases ***
Add Book With Valid Information And Required Fields Filled
    Set Title  Mahtava teksti 
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Book
    Page Should Contain  Book added successfully!

Add Book With Too Short Title
    Set Title    Test
    Set Author  Matti Meikalainen
    Set Year  1999 
    Submit Book
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Book With Required Fields Not Filled
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Book
    Page Should Not Contain  Book added successfully!

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

Submit Book
    Scroll Element Into view  submit
    Click Button  submit