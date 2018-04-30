*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can see all roles in Sharing Tab
  Given a logged-in site administrator
   When I go to sharing view
   Then I can see role 'CatalogAdmin'
    and I can see role 'CommuneEditor'
    and I can see role 'PkanEditor'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator


# --- WHEN -------------------------------------------------------------------

I go to sharing View
  Go To  ${PLONE_URL}/sharing
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

I can see role '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
