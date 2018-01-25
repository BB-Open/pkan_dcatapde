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


*** Variables ****************************************************************

@{DIMENSIONS}  1200  800
