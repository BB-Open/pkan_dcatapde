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

I set the criteria ${type} in row ${number} to the option '${label}'
  [Documentation]  A couple of times we shift the focus so the input sticks, and wait a bit,
  ...              to make the test more stable.
  ${criteria_row} =  Convert to String  .querystring-criteria-wrapper:nth-child(${number})
  Wait until page contains element  css=${criteria_row} .querystring-criteria-${type} .select2-choice
  Click Element  css=${criteria_row} .querystring-criteria-${type} .select2-choice
  Sleep  1.5
  Focus  css=body
  Wait until element is visible  css=#select2-drop input
  Input Text  css=#select2-drop input  ${label}
  Sleep  1.5
  Focus  css=body
  Wait until element is visible  css=#select2-drop .select2-match
  Click Element  css=#select2-drop .select2-match
  Sleep  1.5
  Focus  css=body

I set the criteria ${type} in row ${number} to the options '${label}'
  ${criteria_row} =  Convert to String  .querystring-criteria-wrapper:nth-child(${number})
  Wait until page contains element  css=${criteria_row} .querystring-criteria-${type} .select2-choices
  Click Element  css=${criteria_row} .querystring-criteria-${type} .select2-choices
  Wait until page contains element  css=.select2-input.select2-focused
  Input text  css=.select2-input.select2-focused  ${label}\n
  Sleep  1.5

I set the criteria ${type} in row ${number} to the text '${label}'
  ${criteria_row} =  Convert to String  .querystring-criteria-wrapper:nth-child(${number})
  Input text  css=${criteria_row} .querystring-criteria-value input  ${label}\t
  [Documentation]  Shift the focus so the input sticks, and wait a bit
  Sleep  1.5
  Focus  css=.querystring-sortreverse
  Sleep  1.5

Open PKANWorkflowMenu
    [Arguments]  ${elementId}
    Element Should Be Visible  css=li#${elementId}
    Element Should Not Be Visible  css=li.plonetoolbar-workflow-transition
    Click link  css=li#${elementId} a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=li.plonetoolbar-workflow-transition


I activate the object
  Open PKANWorkflowMenu  pkan_activation
  Click Link  workflow-transition-activate
  Sleep  1.5

*** Variables ****************************************************************

@{DIMENSIONS}  1200  800
