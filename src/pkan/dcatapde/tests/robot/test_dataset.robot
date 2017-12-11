# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_dataset.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_dataset.robot
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

Scenario: As a site administrator I can add a dataset
  Given a logged-in site administrator
    and an add dataset form
   When I type 'My Dataset' into the title field
    and I submit the form
   Then a dataset with the title 'My Dataset' has been created

Scenario: As a site administrator I can view a dataset
  Given a logged-in site administrator
    and a dataset 'My Dataset'
   When I go to the dataset view
   Then I can see the dataset title 'My Dataset'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add dataset form
  Go To  ${PLONE_URL}/++add++dataset

a dataset 'My Dataset'
  Create content  type=dataset  id=my-dataset  title=My Dataset


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the dataset view
  Go To  ${PLONE_URL}/my-dataset
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a dataset with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the dataset title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
