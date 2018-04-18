*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown

Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a concept document
  Given a logged-in site administrator
    and an add skos_concept document form
   When I type 'A Concept' into the title field
    and I type 'A Concept description' into the description field
    and I type 'https://example.com/a-concept' into the concept scheme uri field
    and I type 'https://example.com/this-concept' into the definition uri field
    and take a screenshot 'skos_concept_add_form'
    and I submit the form
   Then a concept document with the title 'A Concept' has been created
    and take a screenshot 'skos_concept_added'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add skos_concept document form
  Go To  ${PLONE_URL}/concepts/++add++skos_concept


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.eng  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.eng  ${description}

I type '${uri}' into the concept scheme uri field
  Input Text  form-widgets-skos_inScheme  ${uri}

I type '${uri}' into the definition uri field
  Input Text  form.widgets.rdfs_isDefinedBy  ${uri}

I submit the form
  Click Button  Save


# --- THEN -------------------------------------------------------------------

a concept document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
#  Page should contain  Item created

take a screenshot '${name}'
  Capture and crop page screenshot
  ...  ${name}.png
  ...  css=body
