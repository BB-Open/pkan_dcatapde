*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a harvester_entity_config
  Given a logged-in Manager
    and a harvester_folder 'My Harvester Folder'
    and a harvester 'My Harvester'
    and an add harvester_entity form
   When I type 'My Harvester Entity' into the title field
    and I submit the form
   Then a harvester_entity_config with the title 'My Harvester Entity' has been created

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in Manager
  Enable autologin as  Manager

an add harvester_entity form
  Go To  ${PLONE_URL}/my-harvesterfolder/my_harvester/++add++harvester_entity

a harvester_folder 'My Harvester Folder'
  Create content  type=harvesterfolder  id=my-harvesterfolder  title=My Harvester Folder

a harvester 'My Harvester'
  Go To  ${PLONE_URL}/my-harvesterfolder/++add++harvester
  I type 'my_harvester' into the title field
  I type 'http://test-uir.de' into the 'harvest source' field
  I select 'RDF/Turtle' from the 'source Format' field
  I submit the form


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form-widgets-IDublinCore-title  ${title}

I type '${uri}' into the 'harvest source' field
  Input Text  form-widgets-url  ${uri}

I select '${choice}' from the 'source Format' field
  Select From List By Label  form-widgets-source_type   ${choice}

I submit the form
  Click Button  Save

I go to the harvester_entity_config view
  Go To  ${PLONE_URL}/my-harvesterfolder/my_harvester/my-harvester_entity
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a harvester_entity_config with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  Entity Config

I can see the harvester_entity_config title '${title}'
  Wait until page contains  Site Map
  Page should contain  Entity Config
