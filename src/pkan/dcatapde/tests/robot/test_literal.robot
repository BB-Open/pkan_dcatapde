# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_literal.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_literal.robot
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

Scenario: As a site administrator I can add a literal
  Given a logged-in site administrator
    and an add literal form
   When I type 'My Literal' into the title field
    and I submit the form
   Then a literal with the title 'My Literal' has been created

Scenario: As a site administrator I can view a literal
  Given a logged-in site administrator
    and a literal 'My Literal'
   When I go to the literal view
   Then I can see the literal title 'My Literal'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add literal form
  Go To  ${PLONE_URL}/++add++literal

a literal 'My Literal'
  Create content  type=literal  id=my-literal  title=My Literal


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the literal view
  Go To  ${PLONE_URL}/my-literal
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a literal with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the literal title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
