*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${ADD_ARTICLE_URL}  http://${SERVER}/add-article
${ADD_BOOK_URL}  http://${SERVER}/add-book
${ADD_INPROCEEDING_URL}  http://${SERVER}/add-inproceedings
${ADD_MISC_URL}  http://${SERVER}/add-misc
${IMPORT_BIBTEX_URL}  http://${SERVER}/import-bibtex
${BROWSER}    chrome
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Articles
    Go To  ${RESET_URL}

Go To Add Article Page
    Go To  ${ADD_ARTICLE_URL}

Go To Add Book Page
    Go To  ${ADD_BOOK_URL}

Go To Add Inproceeding Page
    Go To  ${ADD_INPROCEEDING_URL}

Go To Add Misc Page
    Go To  ${ADD_MISC_URL}

Go To Import BibTeX Page
    Go To  ${IMPORT_BIBTEX_URL}
