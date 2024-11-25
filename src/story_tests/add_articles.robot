*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Article Page

*** Test Cases ***
Add Article With Valid Information
    Set Title  mahtava teksti 
    Set Author  Matti Meikalainen
    Set Journal  jokin lehti
    Set Year  2020
    Submit Article
    Page Should Contain  Article added successfully!

Add Article With Too Short Title
    Set Title  joku
    Set Author  Matti Meikalainen
    Set Journal  nature 
    Set Year  1999 
    Submit Article
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Article With Not All Required Fields Filled
    Set Title  joku
    Set Author  Matti Meikalainen
    Submit Article
    Page Should Not Contain    Article added successfully!


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

