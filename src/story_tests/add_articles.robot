*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Article Page

*** Test Cases ***
Add Article With Valid Information
    Set Title  Can artificial intelligence help for scientific writing?
    Set Author  Salvagno, Michele, Fabio Silvio Taccone, and Alberto Giovanni Gerli 
    Set Journal  Critical care
    Set Year  2023
    Submit Article
    Page Should Contain  Article added successfully!

Add Article With Too Short Title
    Set Title  Can?
    Set Author  Salvagno, Michele
    Set Journal  Critical care 
    Set Year  2023 
    Submit Article
    Page Should Contain  Title must be between 5 and 255 characters. 

Add Article With Not All Required Fields Filled
    Set Title  Can artificial intelligence help for scientific writing?
    Set Author  Salvagno, Michele, Fabio Silvio Taccone, and Alberto Giovanni Gerli 
    Submit Article
    Page Should Not Contain    Article added successfully!

Add Valid Article With All Inputs
    Set Title  Time, Clocks, and the Ordering of Events in a Distributed System
    Set Author  Leslie Lamport
    Set Journal  Communications of the ACM
    Set Year  1978
    Set Volume  21
    Set Number  7
    Set Pages  558-565
    Set Month  July
    Set Doi  10.1145/359545.359563
    Submit Article
    Page Should Contain    Article added successfully!

Add Valid Article Containing All Allowed Character Types And Multiple Authors
    Set Title  Toimitusketjujen Optimointi
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

