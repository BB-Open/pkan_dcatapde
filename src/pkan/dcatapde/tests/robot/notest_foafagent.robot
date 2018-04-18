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
    and I type 'https://example.com/publisher' into the access uri field
    and I submit the form
   Then a foafagent with the title 'My FOAFAgent' has been created

Scenario: As a site administrator I can view a foafagent
  Given a logged-in site administrator
    and a foafagent 'My FOAFAgent'
   When I go to the foafagent view
   Then I can see the foafagent title 'My FOAFAgent'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add foafagent form
  Go To  ${PLONE_URL}/++add++foafagent

a foafagent 'My FOAFAgent'
  Create content
  ...  type=foafagent
  ...  id=my-foafagent
  ...  title=My FOAFAgent
  ...  description=A description
  ...  rdf_about=https://example.com/my-foafagent


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.dct_title.i18n.eng  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.i18n.eng  ${description}

I type '${rdf_about}' into the access uri field
  Input Text  form.widgets.rdf_about  ${rdf_about}

I submit the form
  Click Button  Save

I go to the foafagent view
  Go To  ${PLONE_URL}/my-foafagent
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a foafagent with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the foafagent title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
