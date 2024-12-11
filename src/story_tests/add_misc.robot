*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Add Misc Page

*** Test Cases ***
Add Misc With Valid Information And Required Fields Filled
    Set Title  Deep learning 
    Set Author  LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey
    Set Year  2015
    Submit Misc
    Page Should Contain  Misc added successfully!

Add Misc With Required Fields Not Filled
    Set Title   Testi
    Set Author  Matti Meikalainen
    Submit Misc
    Page Should Not Contain  Misc added successfully!

Add Misc With All Fields Filled
    Set Title  ImageNet Classification with Deep Convolutional Neural Networks
    Set Author  Krizhevsky, Alex and Sutskever, Ilya and Hinton, Geoffrey E
    Set Year  2012
    Set Month  July
    Set Howpublished  \url{http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf}
    Set Note  Tämä tutkimus esittelee AlexNet-nimisen syvän konvolutionaalisen neuroverkon, joka saavutti merkittäviä tuloksia ImageNet-kuvantunnistuskilpailussa ja oli merkittävä edistysaskel syvän oppimisen alalla.
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

Set Month 
      [Arguments]  ${Month}
      Input Text  month  ${Month}

Set Howpublished 
      [Arguments]  ${Howpublished}
      Input Text  howpublished  ${Howpublished}

Set Note 
      [Arguments]  ${Note}
      Input Text  note  ${Note}

Submit Misc
    Scroll Element Into view  submit
    Click Button  submit