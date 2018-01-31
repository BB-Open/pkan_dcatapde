*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a harvester
  Given a logged-in site administrator
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I submit the form
   Then a harvester with the title 'My Harvester' has been created

Scenario: As a site administrator I can view a harvester
  Given a logged-in site administrator
    and a harvester 'My Harvester'
   When I go to the harvester view
   Then I can see the harvester title 'My Harvester'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add harvester form
  Go To  ${PLONE_URL}/++add++harvester

a harvester 'My Harvester'
  Create content  type=harvester  id=my-harvester  title=My Harvester


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the harvester view
  Go To  ${PLONE_URL}/my-harvester
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a harvester with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the harvester title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
