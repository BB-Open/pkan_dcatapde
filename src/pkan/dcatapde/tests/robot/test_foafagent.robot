# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_foafagent.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_foafagent.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a foafagent
  Given a logged-in site administrator
    and an add foafagent form
   When I type 'My FOAFAgent' into the title field
    and I submit the form
   Then a foafagent with the title 'My FOAFAgent' has been created

Scenario: As a site administrator I can view a foafagent
  Given a logged-in site administrator
    and a foafagent 'My FOAFAgent'
   When I go to the foafagent view
   Then I can see the foafagent title 'My FOAFAgent'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add foafagent form
  Go To  ${PLONE_URL}/++add++foafagent

a foafagent 'My FOAFAgent'
  Create content  type=foafagent  id=my-foafagent  title=My FOAFAgent


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the foafagent view
  Go To  ${PLONE_URL}/my-foafagent
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a foafagent with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the foafagent title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
