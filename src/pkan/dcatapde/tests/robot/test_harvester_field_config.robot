# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_harvester_field_config.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_harvester_field_config.robot
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

Scenario: As a site administrator I can add a harvester_field_config
  Given a logged-in site administrator
    and an add harvester_field_config form
   When I type 'My Harvester Field Config' into the title field
    and I submit the form
   Then a harvester_field_config with the title 'My Harvester Field Config' has been created

Scenario: As a site administrator I can view a harvester_field_config
  Given a logged-in site administrator
    and a harvester_field_config 'My Harvester Field Config'
   When I go to the harvester_field_config view
   Then I can see the harvester_field_config title 'My Harvester Field Config'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add harvester_field_config form
  Go To  ${PLONE_URL}/++add++harvester_field_config

a harvester_field_config 'My Harvester Field Config'
  Create content  type=harvester_field_config  id=my-harvester_field_config  title=My Harvester Field Config


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the harvester_field_config view
  Go To  ${PLONE_URL}/my-harvester_field_config
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a harvester_field_config with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the harvester_field_config title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
