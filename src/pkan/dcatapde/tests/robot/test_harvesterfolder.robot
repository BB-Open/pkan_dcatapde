# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_harvesterfolder.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_harvesterfolder.robot
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

Scenario: As a site administrator I can add a harvesterfolder
  Given a logged-in site administrator
    and an add harvesterfolder form
   When I type 'My HarvesterFolder' into the title field
    and I submit the form
   Then a harvesterfolder with the title 'My HarvesterFolder' has been created

Scenario: As a site administrator I can view a harvesterfolder
  Given a logged-in site administrator
    and a harvesterfolder 'My HarvesterFolder'
   When I go to the harvesterfolder view
   Then I can see the harvesterfolder title 'My HarvesterFolder'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add harvesterfolder form
  Go To  ${PLONE_URL}/++add++harvesterfolder

a harvesterfolder 'My HarvesterFolder'
  Create content  type=harvesterfolder  id=my-harvesterfolder  title=My HarvesterFolder


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the harvesterfolder view
  Go To  ${PLONE_URL}/my-harvesterfolder
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a harvesterfolder with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the harvesterfolder title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
