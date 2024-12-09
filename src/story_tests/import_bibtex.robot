*** Settings ***
Resource  resource.robot 
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Import BibTeX Page
    
*** Test Cases ***
Import BibTeX for Article
    Set BibTex  @article{kao2024robodebt, title={From Robodebt to responsible AI: sociotechnical imaginaries of AI in Australia}, author={Kao, Kai-Ti}, journal={Communication Research and Practice}, pages={1-11}, year={2024}, publisher={Taylor \& Francis}}
    Submit Bibtex
    Page Should Contain  Article 'From Robodebt to responsible AI: sociotechnical imaginaries of AI in Australia' imported successfully!

Import BibTeX for Book
    Set BibTex  @book{gusfield1997algorithms, title={Algorithms on stings, trees, and sequences: Computer science and computational biology}, author={Gusfield, Dan}, journal={Acm Sigact News}, volume={28}, number={4}, pages={41-60}, year={1997}, publisher={ACM New York, NY, USA}}
    Submit Bibtex
    Page Should Contain  Book 'Algorithms on stings, trees, and sequences: Computer science and computational biology' imported successfully!

Import BibTeX for Inproceeding
    Set BibTex  @inproceedings{ley2002dblp, title={The DBLP computer science bibliography: Evolution, research issues, perspectives}, author={Ley, Michael}, booktitle={International symposium on string processing and information retrieval}, pages={1-10}, year={2002}, organization={Springer} }
    Submit Bibtex
    Page Should Contain  Inproceedings 'The DBLP computer science bibliography: Evolution, research issues, perspectives' imported successfully!

Import BibTeX for Misc
    Set BibTex  @misc{Nakamoto2008, author = {Satoshi Nakamoto}, title = {Bitcoin: A Peer-to-Peer Electronic Cash System}, year = {2008}, howpublished = {Online}, note = {Accessed: 2021-09-01}, url = {https://bitcoin.org/bitcoin.pdf}}
    Submit Bibtex
    Page Should Contain  Misc 'Bitcoin: A Peer-to-Peer Electronic Cash System' imported successfully!

Import BibTeX Author Missing 
    Set BibTex  @misc{Nakamoto2008, title = {Bitcoin: A Peer-to-Peer Electronic Cash System}, year = {2008}, howpublished = {Online}, note = {Accessed: 2021-09-01}, url = {https://bitcoin.org/bitcoin.pdf}}
    Submit Bibtex
    Page Should Contain  Author is required.    

Import BibTeX Title Too Short  
    Set BibTex  @article{kao2024robodebt, title={F}, author={Kao, Kai-Ti}, journal={Communication Research and Practice}, pages={1-11}, year={2024}, publisher={Taylor \& Francis}}
    Submit Bibtex
    Page Should Contain  Title must be between 5 and 255 characters.

Import BibTeX Article Journal Missing 
    Set BibTex  @article{pool2023ai, title={An AI-Enabled Community Safety Service: Stakeholder Benefits and Vulnerabilities}, author={Pool, Javad and Smith, Natalie and Dodds, Hunter and Lockey, Steven and Curtis, Caitlin and Rinta-Kahila, Tapani and Gillespie, Nicole}, year={2023}}
    Submit Bibtex
    Page Should Contain  Journal is required.

Import BibTeX Year In The Future  
    Set BibTex  @misc{Nakamoto2008, author = {Satoshi Nakamoto}, title = {Bitcoin: A Peer-to-Peer Electronic Cash System}, year = {2800}, howpublished = {Online}, note = {Accessed: 2021-09-01}, url = {https://bitcoin.org/bitcoin.pdf}}
    Submit Bibtex
    Page Should Contain  Year must be a valid number between 0 and 2100


*** Keywords ***
Set BibTex
    [Arguments]  ${bibtex}
    Input Text  bibtex_text  ${bibtex}
    
Submit Bibtex
    Scroll Element Into view  submit
    Click Button  submit

