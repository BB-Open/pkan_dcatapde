*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a foafagent
  Given a logged-in site administrator
    and an add foafagent form
   When I type 'My FOAFAgent' into the title field
    and I type 'A description' into the description field
    and I type 'https://example.com/publisher' into the isDefinedBy uri field
    and I submit the form
   Then a foafagent with the title 'My FOAFAgent' has been created


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add foafagent form
  Go To  ${PLONE_URL}/agents/++add++foaf_agent


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.eng  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.eng  ${description}

I type '${uri}' into the isDefinedBy uri field
  Input Text  form-widgets-rdfs_isDefinedBy  ${uri}

I submit the form
  Click Button  Save

I go to the foafagent view
  Go To  ${PLONE_URL}/agents/my-foafagent
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a foafagent with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
#  Page should contain  Item created

I can see the foafagent title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
