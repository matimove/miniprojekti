*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Inproceeding Page

*** Test Cases ***
Add Inproceedings With Valid Information And Required Fields Filled
    Set Title  MapReduce: Simplified Data Processing on Large Clusters 
    Set Author  Jeffrey Dean and Sanjay Ghemawat
    Set Booktitle   Proceedings of the 6th Conference on Symposium on Opearting Systems Design and Implementation - Volume 6
    Set Year  2004
    Submit Inproceedings
    Page Should Contain  Inproceedings added successfully!

Add Inproceedings With Too Short Title
    Set Title    Map
    Set Author  Jeffrey Dean and Sanjay Ghemawat
    Set Booktitle    Proceedings of the 6th Conference 
    Set Year  2004
    Submit Inproceedings
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Inproceedings With Required Fields Not Filled
    Set Author  Jeffrey Dean and Sanjay Ghemawat
    Set Year    2004
    Submit Inproceedings
    Page Should Not Contain  Inproceedings added successfully!

Add Inproceedings With All Fields Filled
    Set Title  The Google File System
    Set Author  Sanjay Ghemawat and Howard Gobioff and Shun-Tak Leung
    Set Booktitle   Proceedings of the Nineteenth ACM Symposium on Operating Systems Principles
    Set Year  2003
    Set Editor  Mary Baker
    Set Volume  37
    Set Number  5
    Set Series  SOSP '03
    Set Pages  29-43
    Set Address  Bolton Landing, NY, USA
    Set Month  Oct
    Set Organization  ACM
    Set Publisher  ACM Press
    Submit Inproceedings
    Page Should Contain  Inproceedings added successfully!


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

Set Editor
      [Arguments]  ${Editor}
      Input Text  booktitle  ${Editor}

Set Volume
      [Arguments]  ${Volume}
      Input Text  booktitle  ${Volume}

Set Number
      [Arguments]  ${Number}
      Input Text  booktitle  ${Number}

Set Series
      [Arguments]  ${Series}
      Input Text  booktitle  ${Series}

Set Pages
      [Arguments]  ${Pages}
      Input Text  booktitle  ${Pages}

Set Address
      [Arguments]  ${Address}
      Input Text  booktitle  ${Address}

Set Month
      [Arguments]  ${Month}
      Input Text  booktitle  ${Month}

Set Organization
      [Arguments]  ${Organization}
      Input Text  booktitle  ${Organization}

Set Publisher
      [Arguments]  ${Publisher}
      Input Text  booktitle  ${Publisher}

Submit Inproceedings
    Scroll Element Into view  submit
    Click Button  submit