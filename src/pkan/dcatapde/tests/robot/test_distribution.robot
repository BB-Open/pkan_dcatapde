*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a distribution
  Given a logged-in site administrator
    and an add distribution form
   When I type 'My Distribution' into the title field
    and I submit the form
   Then a distribution with the title 'My Distribution' has been created

Scenario: As a site administrator I can view a distribution
  Given a logged-in site administrator
    and a distribution 'My Distribution'
   When I go to the distribution view
   Then I can see the distribution title 'My Distribution'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add distribution form
  Go To  ${PLONE_URL}/++add++distribution

a distribution 'My Distribution'
  Create content  type=distribution  id=my-distribution  title=My Distribution


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the distribution view
  Go To  ${PLONE_URL}/my-distribution
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a distribution with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the distribution title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
