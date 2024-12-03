*** Settings ***
Resource  resource.robot 
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Misc Page

*** Test Cases ***
Generate BibTeX for Article
    Go To Add Article Page
    Set Title  D mahtava teksti
    Set Author  Matti Meikalainen
    Set Journal  jokin lehti
    Set Year  2020
    Submit Article
    Set Search  D mahtava teksti
    Submit Search
    Click Button  Generate BibTeX
    Article BibTeX Content Should Be Correct

Generate BibTeX for Book
    Go To Add Book Page
    Set Title  C mahtava teksti
    Set Author  Matti Meikalainen
    Set Year  2020
    Submit Book
    Set Search  C mahtava teksti
    Submit Search
    Click Button  Generate BibTeX
    Book BibTeX Content Should Be Correct

Generate BibTeX for Inproceedings
    Go To Add Inproceeding Page
    Set Author  Matti Meikalainen
    Set Title  B mahtava teksti
    Set Booktitle  jokin konferenssi
    Set Year  2020
    Submit Inproceedings
    Set Search  B mahtava teksti
    Submit Search
    Click Button  Generate BibTeX
    Inproceedings BibTeX Content Should Be Correct

Generate BibTeX for Misc
    Go To Add Misc Page
    Set Title  A mahtava teksti
    Set Author  Matti Meikalainen
    Set Year  2020
    Submit Misc
    Set Search  A mahtava teksti
    Submit Search
    Click Button  Generate BibTeX
    Misc BibTeX Content Should Be Correct

*** Keywords ***
Set Search 
    [Arguments]  ${search}
    Input Text  search  ${search}

Submit Search
    Scroll Element Into View  search-button
    Click Button  search-button

Article BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Matti Meikalainen"
    Should Contain  ${bibtex}  title = "D mahtava teksti"
    Should Contain  ${bibtex}  journal = "jokin lehti"
    Should Contain  ${bibtex}  year = "2020"

Book BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Matti Meikalainen"
    Should Contain  ${bibtex}  title = "C mahtava teksti"
    Should Contain  ${bibtex}  year = "2020"

Inproceedings BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Matti Meikalainen"
    Should Contain  ${bibtex}  title = "B mahtava teksti"
    Should Contain  ${bibtex}  Booktitle = "jokin konferenssi"
    Should Contain  ${bibtex}  year = "2020"

Misc BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Matti Meikalainen"
    Should Contain  ${bibtex}  title = "A mahtava teksti"
    Should Contain  ${bibtex}  year = "2020"

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

Set Booktitle
    [Arguments]  ${booktitle}
    Input Text  booktitle  ${booktitle}

Submit Article
    Scroll Element Into View  submit
    Click Button  submit

Submit Misc
    Scroll Element Into View  submit
    Click Button  submit

Submit Book
    Scroll Element Into View  submit
    Click Button  submit

Submit Inproceedings
    Scroll Element Into View  submit
    Click Button  submit
