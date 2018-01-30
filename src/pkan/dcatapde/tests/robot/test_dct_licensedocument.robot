*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown

Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a license document
  Given a logged-in site administrator
    and an add license document form
   When I type 'A License' into the title field
    and I type 'A license description' into the description field
    and I type 'https://example.com/a-license' into the access uri field
    and take a screenshot 'dct_licensedocument_add_form'
    and I submit the form
   Then a license document with the title 'A License' has been created
    and take a screenshot 'dct_licensedocument_added'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add license document form
  Go To  ${PLONE_URL}/licenses/++add++dct_licensedocument


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.dct_title.i18n.en  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.i18n.en  ${description}

I type '${uri}' into the access uri field
  Input Text  form.widgets.rdf_about  ${uri}

I submit the form
  Click Button  Save


# --- THEN -------------------------------------------------------------------

a license document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

take a screenshot '${name}'
  Capture and crop page screenshot
  ...  ${name}.png
  ...  css=body
