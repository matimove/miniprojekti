*** Settings ***
Resource  resource.robot 
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Misc Page

*** Test Cases ***
Generate BibTeX for Article
    Go To Add Article Page
    Set Title  Reducing the dimensionality of data with neural networks
    Set Author  Hinton, Geoffrey E and Salakhutdinov, Ruslan R
    Set Journal  Science
    Set Year  2006
    Submit Article
    Set Search  Reducing the dimensionality of data with neural networks
    Submit Search
    Scroll Element Into View  generate-bibtex-button
    Click Button  generate-bibtex-button
    Wait Until Element Is Visible  //textarea[@class="form-control" and @readonly]
    Article BibTeX Content Should Be Correct

Generate BibTeX for Book
    Go To Add Book Page
    Set Title  Pattern Recognition and Machine Learning
    Set Author  Bishop, Christopher M
    Set Year  2006
    Submit Book
    Set Search  Pattern Recognition and Machine Learning
    Submit Search
    Scroll Element Into View  generate-bibtex-button
    Click Button  generate-bibtex-button
    Wait Until Element Is Visible  //textarea[@class="form-control" and @readonly]
    Book BibTeX Content Should Be Correct

# Generate BibTeX for Inproceedings
#     Go To Add Inproceeding Page
#     Set Author  LeCun, Yann et. al.
#     Set Title  Backpropagation applied to handwritten zip code recognition
#     Set Booktitle  Neural computation
#     Set Year  1989
#     Submit Inproceedings
#     Set Search  Backpropagation applied to handwritten zip code recognition
#     Submit Search
#     Scroll Element Into View  generate-bibtex-button
#     Click Button  generate-bibtex-button
#     Wait Until Element Is Visible  //textarea[@class="form-control" and @readonly]
#     Inproceedings BibTeX Content Should Be Correct
# 
# Generate BibTeX for Misc
#     Go To Add Misc Page
#     Set Title  Mastering the game of Go with deep neural networks and tree search
#     Set Author  Silver, David et. al.
#     Set Year  2016
#     Submit Misc
#     Set Search  Mastering the game of Go with deep neural networks and tree search
#     Submit Search
#     Scroll Element Into View  generate-bibtex-button
#     Click Button  generate-bibtex-button
#     Wait Until Element Is Visible  //textarea[@class="form-control" and @readonly]
#     Misc BibTeX Content Should Be Correct

*** Keywords ***
Set Search 
    [Arguments]  ${search}
    Input Text  search  ${search}

Submit Search
    Scroll Element Into View  search-button
    Click Button  search-button

Article BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Hinton, Geoffrey E and Salakhutdinov, Ruslan R"
    Should Contain  ${bibtex}  title = "Reducing the dimensionality of data with neural networks"
    Should Contain  ${bibtex}  journal = "Science"
    Should Contain  ${bibtex}  year = "2006"

Book BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Bishop, Christopher M"
    Should Contain  ${bibtex}  title = "Pattern Recognition and Machine Learning"
    Should Contain  ${bibtex}  year = "2006"

Inproceedings BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "LeCun, Yann et. al."
    Should Contain  ${bibtex}  title = "Backpropagation applied to handwritten zip code recognition"
    Should Contain  ${bibtex}  year = "1989"

Misc BibTeX Content Should Be Correct
    ${bibtex}=  Get Text  //textarea[@class="form-control" and @readonly]
    Should Contain  ${bibtex}  author = "Silver, David et. al."
    Should Contain  ${bibtex}  year = "2016"

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
