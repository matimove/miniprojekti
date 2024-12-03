*** Settings ***
Resource  resource.robot 
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup    Go To  ${HOME_URL}

*** Test Cases ***
Search Successful When Keyword In Reference Title
    Go To Add Book Page
    Set Title  Introduction to the theory of computation
    Set Author  Michael Sipser
    Set Year    2013
    Submit Book
    Go To Add Book Page
    Set Title  Operating systems: internals and design principles
    Set Author    William Stallings
    Set Year    2018
    Submit Book
    Set Search    computation
    Submit Search
    Page Should Contain  Introduction to the theory of computation
    Page Should Not Contain    Operating systems: internals and design principles

Search Successful When Keyword In Reference Author
    Set Search    William
    Submit Search
    Page Should Contain  Operating systems: internals and design principles
    Page Should Not Contain    Introduction to the theory of computation

Search Successful When Keyword In Reference Year
    Set Search    2018
    Submit Search
    Page Should Contain  Operating systems: internals and design principles
    Page Should Not Contain    Introduction to the theory of computation


Search Unsuccessful When Keyword Is Not Found In Any Reference
    Set Search    unsuccesfull search test
    Submit Search
    Page Should Contain    (0) results found for unsuccesfull search test


*** Keywords ***
Set Search 
    [Arguments]  ${search}
    Input Text  search  ${search}

Submit Search
    Scroll Element Into view  search-button
    Click Button  search-button

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