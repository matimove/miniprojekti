*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Inproceeding Page

*** Test Cases ***
Add Inproceedings With Valid Information And Required Fields Filled
    Set Title  Mahtava teksti 
    Set Author  Matti Meikalainen
    Set Booktitle    Booktitle
    Set Year    2024
    Submit Inproceedings
    Page Should Contain  Inproceedings added successfully!

Add Inproceedings With Too Short Title
    Set Title    Test
    Set Author  Matti Meikalainen
    Set Booktitle    Booktitle
    Set Year  1999 
    Submit Inproceedings
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Inproceedings With Required Fields Not Filled
    Set Author  Matti Meikalainen
    Set Year    2024
    Submit Inproceedings
    Page Should Not Contain  Inproceedings added successfully!

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

Set Booktitle
      [Arguments]  ${Booktitle}
      Input Text  booktitle  ${booktitle}

Submit Inproceedings
    Scroll Element Into view  submit
    Click Button  submit