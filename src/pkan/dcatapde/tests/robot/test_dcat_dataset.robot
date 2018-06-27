*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a dataset
  Given a logged-in site administrator
    and a catalog 'My Catalog'
    and an add dataset form
   When I type 'My Dataset' into the title field
    and I type 'a dataset' into the description field
    and I submit the form
   Then a dataset with the title 'My Dataset' has been created


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

a catalog 'My Catalog'
  Create content  type=dcat_catalog  id=my-catalog  title=My Catalog

an add dataset form
  Go To  ${PLONE_URL}/my-catalog/++add++dcat_dataset


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.eng  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.eng  ${description}

I submit the form
  Click Button  Save

I go to the dataset view
  Go To  ${PLONE_URL}/my-dataset
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a dataset with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
#  Page should contain  Item created

I can see the dataset title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
