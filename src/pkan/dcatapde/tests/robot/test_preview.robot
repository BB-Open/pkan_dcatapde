*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown

*** Variables ***
${query} =
...  SELECT DISTINCT ?license ?label ?definition
...  WHERE {
...     ?license rdfs:isDefinedBy ?definition .
...     ?license rdfs:label ?label .
...  }

*** Test Cases ***

Scenario: As a manager I can call preview
  Given a logged-in manager
   When I go to the preview
   Then I can see the preview 'Did not find correct parameters to request data.'

Scenario: As a manager I can call preview on harvester
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and a harvester 'My Harvester'
   When I go to the preview on harvester
   Then I can see the preview 'Did not find correct parameters to request data.'

Scenario: As a manager I can call preview with url and source_type
  Given a logged-in manager
   When I go to the preview and add query 'form.widgets.url=http://www.example.de&form.widgets.source_type=rdf-xml'
   Then I can see the preview 'Could not read source.'

Scenario: As a manager I can call preview on harvester with url and source_type
  Given a logged-in manager
    and a harvester folder 'Harvester Folder'
    and a harvester 'My Harvester'
   When I go to the preview on harvester and add query 'form.widgets.url=http://www.example.de&form.widgets.source_type=rdf-xml'
   Then I can see the preview 'Could not read source.'

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in manager
  Enable autologin as  Manager

a harvester folder 'Harvester Folder'
  Create content  type=harvesterfolder  id=my-harvesterfolder  title=My HarvesterFolder

a harvester 'My Harvester'
  Create content
  ...  type=harvester
  ...  id=my-harvester
  ...  title=My Harvester
  ...  container=/plone/my-harvesterfolder
  ...  url=https://example.com

# --- WHEN -------------------------------------------------------------------

I click the button '${button}'
  Click Button  ${button}

I go to the preview
  Go To  ${PLONE_URL}/harvester_preview

I go to the preview and add query '${query}'
  Go To  ${PLONE_URL}/harvester_preview?${query}

I go to the preview on harvester
  Go To  ${PLONE_URL}/my-harvesterfolder/my-harvester/harvester_preview

I go to the preview on harvester and add query '${query}'
  Go To  ${PLONE_URL}/my-harvesterfolder/my-harvester/harvester_preview?${query}

# --- THEN -------------------------------------------------------------------

I can see the preview '${preview}'
  Wait until page contains  Result:
  Page should contain  ${preview}
