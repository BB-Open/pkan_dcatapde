# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pkan.dcatapde -t test_catalog.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pkan.dcatapde.testing.PKAN_DCATAPDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_catalog.robot
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

Scenario: As a site administrator I can add a catalog
  Given a logged-in site administrator
    and an add catalog form
   When I type 'My Catalog' into the title field
    and I submit the form
   Then a catalog with the title 'My Catalog' has been created

Scenario: As a site administrator I can view a catalog
  Given a logged-in site administrator
    and a catalog 'My Catalog'
   When I go to the catalog view
   Then I can see the catalog title 'My Catalog'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add catalog form
  Go To  ${PLONE_URL}/++add++catalog

a catalog 'My Catalog'
  Create content  type=catalog  id=my-catalog  title=My Catalog


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the catalog view
  Go To  ${PLONE_URL}/my-catalog
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a catalog with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the catalog title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
