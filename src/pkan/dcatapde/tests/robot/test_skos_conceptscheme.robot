*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown

Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a concept scheme document
  Given a logged-in site administrator
    and an add skos_conceptscheme document form
   When I type 'A Concept Scheme' into the title field
    and I type 'A Concept Scheme description' into the description field
    and I type 'https://example.com/a-concept-scheme' into the definition uri field
    and take a screenshot 'skos_conceptscheme_add_form'
    and I submit the form
   Then a concept scheme document with the title 'A Concept Scheme' has been created
    and take a screenshot 'skos_conceptscheme_added'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add skos_conceptscheme document form
  Go To  ${PLONE_URL}/conceptschemes/++add++skos_conceptscheme


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.en  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.en  ${description}

I type '${uri}' into the definition uri field
  Input Text  form.widgets.rdfs_isDefinedBy  ${uri}

I submit the form
  Click Button  Save


# --- THEN -------------------------------------------------------------------

a concept scheme document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

take a screenshot '${name}'
  Capture and crop page screenshot
  ...  ${name}.png
  ...  css=body
