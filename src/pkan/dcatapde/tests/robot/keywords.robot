*** Settings *****************************************************************

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/server.robot
Resource  Selenium2Screenshots/keywords.robot

Variables  plone/app/testing/interfaces.py


*** Keywords *****************************************************************

Setup
    Setup Plone site  pkan.dcatapde.testing.ACCEPTANCE_TESTING
    Import library  Remote  ${PLONE_URL}/RobotRemote
    Run keyword and ignore error  Set window size  @{DIMENSIONS}

Teardown
    Teardown Plone Site

I select '${choice}' from an AJAX select widget with id '${field}'
    Wait until page contains element  css=#${field} .select2-choices
    Click Element  css=#${field} .select2-choices
    Sleep  1.5
    Focus  css=body
    Wait until element is visible  css=#${field} .select2-choices input
    Input Text  css=#${field} .select2-choices input  ${choice}
    Sleep  1.5
    Focus  css=body
    Wait until element is visible  css=#select2-drop .select2-match
    Click Element  css=#select2-drop .select2-match
    Sleep  1.5
    Focus  css=body

I select '${value}' in '${field}'
    Select From List  name=${field}:list  ${value}



*** Variables ****************************************************************

@{DIMENSIONS}  1200  800
