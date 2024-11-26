*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Misc Page

*** Test Cases ***
Add Misc With Valid Information And Required Fields Filled
    Set Title  Mahtava teksti 
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Misc
    Page Should Contain  Misc added successfully!

Add Misc With Too Short Title
    Set Title    Test
    Set Author  Matti Meikalainen
    Set Year  1999
    Submit Misc
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Misc With Required Fields Not Filled
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Misc
    Page Should Not Contain  Misc added successfully!

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

Submit Misc
    Scroll Element Into view  submit
    Click Button  submit