*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a manager I can add a harvester
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
   Then a harvester with the title 'My Harvester' has been created

Scenario: As a manager I can view a harvester
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to the harvester view
   Then I can see the harvester title 'My Harvester'

Scenario: As a manager I can view a harvester on folder_view
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to harvester folder view
   Then I can see the harvester title 'My Harvester'

Scenario: As a manager I can view a harvester on control_panel
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to controlpanel view
   Then I can see the harvester title 'My Harvester'

Scenario: As a manager I can view harvester_entity-View
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to harvester_entity view
   Then I can see the harvester title 'My Harvester'

Scenario: As a manager I can request preview data on harvester_entity-view
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to harvester_entity view
    and I click the button 'Run'
   Then I can see the harvester title 'My Harvester'
    and I can see the preview 'Not Found'

Scenario: As a manger I can submit data on harvester_entity-view
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and an add harvester form
   When I type 'My Harvester' into the title field
    and I type 'http://www.test.de' into the url field
    and I submit the form
    and I go to harvester_entity view
    and I submit the form
   Then I can see the harvester title 'My Harvester'
    and I can see the success message 'Thank you very much!'

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in manager
  Enable autologin as  Manager

a harvester folder 'Harvester Folder'
  Create content  type=harvesterfolder  id=my-harvesterfolder  title=My HarvesterFolder

an add harvester form
  Go To  ${PLONE_URL}/my-harvesterfolder/++add++harvester



# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I type '${url}' into the url field
  Input Text  name=form.widgets.url  ${url}

I submit the form
  Click Button  Save

I click the button '${button}'
  Click Button  ${button}

I go to the harvester view
  Go To  ${PLONE_URL}/my-harvesterfolder/my-harvester
  Wait until page contains  Site Map

I go to harvester folder view
  Go To  ${PLONE_URL}/my-harvesterfolder/harvester_overview
  Wait until page contains  Site Map

I go to controlpanel view
  Go To  ${PLONE_URL}/harvester_overview
  Wait until page contains  Site Map

I go to harvester_entity view
  Go To  ${PLONE_URL}/my-harvesterfolder/my-harvester/harvester_entity
  Wait until page contains  Site Map

# --- THEN -------------------------------------------------------------------

a harvester with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the harvester title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

I can see the success message '${message}'
  Wait until page contains  Site Map
  Page should contain  ${message}

I can see the preview '${preview}'
  Wait until page contains  Site Map
  Page should contain  ${preview}
