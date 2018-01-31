*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a dataset
  Given a logged-in site administrator
    and an add dataset form
   When I type 'My Dataset' into the title field
    and I submit the form
   Then a dataset with the title 'My Dataset' has been created

Scenario: As a site administrator I can view a dataset
  Given a logged-in site administrator
    and a dataset 'My Dataset'
   When I go to the dataset view
   Then I can see the dataset title 'My Dataset'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add dataset form
  Go To  ${PLONE_URL}/++add++dact_dataset

a dataset 'My Dataset'
  Create content  type=dact_dataset  id=my-dataset  title=My Dataset


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text name=form.widgets.dct_title.i18n.en ${title}

I submit the form
  Click Button  Save

I go to the dataset view
  Go To  ${PLONE_URL}/my-dataset
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a dataset with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the dataset title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
