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

Add Valid Article With All Inputs
    Set Title  Toimitusketjujen Optimointi
    Set Author  Joulupukki
    Set Journal  Joulutiede Journal
    Set Year  2024
    Set Volume  1
    Set Number  1
    Set Pages  1-10
    Set Month  December
    Set Doi  10.1234/example-doi
    Submit Article
    Page Should Contain    Article added successfully!

Add Valid Article Containing All Allowed Character Types And Multiple Authors
    Set Title  Monien tekijöiden artikkeli
    Set Author  Joulupukki, Joulumuori, Tonttu T. Toljanteri, Petteri Punakuono, Iso-Tonttu, Ääkkösmies Å. Öökkölä
    Set Journal  Joulutiede Journal
    Set Year  2024
    Set Volume  1
    Set Number  2
    Set Pages  123-130
    Set Month  December
    Set Doi  10.1234/example-doi
    Submit Article
    Page Should Contain    Article added successfully!

Add Real Article
    Set Title  Implementation of the EU AI act calls for interdisciplinary governance
    Set Author  Huixin Zhong
    Set Journal  AI Magazine
    Set Year  2024
    Set Volume  45
    Set Number  3
    Set Pages  333-337
    Set Month  July
    Set Doi  10.1002/aaai.12183
    Submit Article
    Page Should Contain    Article added successfully!

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

Set Volume
      [Arguments]  ${volume}
      Input Text  volume  ${volume}

Set Number
      [Arguments]  ${number}
      Input Text  number  ${number}

Set Pages
      [Arguments]  ${pages}
      Input Text  pages  ${pages}

Set Month
      [Arguments]  ${month}
      Input Text  month  ${month}

Set Doi
      [Arguments]  ${doi}
      Input Text  doi  ${doi}

Submit Article
    Scroll Element Into view  submit
    Click Button  submit

