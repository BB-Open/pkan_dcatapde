*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a catalog
  Given a logged-in site administrator
    and an add catalog form
   When I type 'My Catalog' into the title field
    and I type 'A description' into the description field
    and I submit the form
   Then a catalog with the title 'My Catalog' has been created

Scenario: As a site administrator I can view a catalog
  Given a logged-in site administrator
    and a publisher 'Publisher'
    and a catalog 'My Catalog'
   When I go to the catalog view
   Then I can see the catalog title 'My Catalog'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add catalog form
  Go To  ${PLONE_URL}/++add++dcat_catalog

a catalog 'My Catalog'
  Create content  type=dcat_catalog  id=my-catalog  title=My Catalog

a publisher 'Publisher'
  Create content  type=foaf_agent  id=publisher  title=Publisher



# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.dct_title.i18n.en  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.i18n.en  ${description}

I submit the form
  Click Button  Save

I go to the catalog view
  Go To  ${PLONE_URL}/my-catalog
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a catalog with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the catalog title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
