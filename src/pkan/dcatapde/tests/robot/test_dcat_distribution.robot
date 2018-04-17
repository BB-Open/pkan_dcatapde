*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a distribution
  Given a logged-in site administrator
    and a catalog 'My Catalog'
    and a dataset 'My Dataset'
    and an add distribution form
   When I type 'My DCATDistribution' into the title field
    and I submit the form
   Then a distribution with the title 'My DCATDistribution' has been created


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add distribution form
  Go To  ${PLONE_URL}/my-catalog/my-dataset/++add++dcat_distribution

a catalog 'My Catalog'
  Create content  type=dcat_catalog  id=my-catalog  title=My Catalog

a dataset 'My Dataset'
  Create content  type=dcat_dataset  id=my-dataset  title=My Dataset  container=/plone/my-catalog


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.dct_title.i18n.en  ${title}

I submit the form
  Click Button  Save

I go to the distribution view
  Go To  ${PLONE_URL}/my-distribution
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a distribution with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
#  Page should contain  Item created

I can see the distribution title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
