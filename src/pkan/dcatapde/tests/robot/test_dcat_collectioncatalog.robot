*** Settings *****************************************************************

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a collectioncatalog
  Given a logged-in site administrator
    and a publisher 'Test-Publisher'
    and an add collectioncatalog form
   When I type 'My CollectionCatalog' into the title field
    and I type 'A description' into the description field
    and I select 'Test-Publisher' from an AJAX select widget with id 'formfield-form-widgets-dct_publisher'
    and I submit the form
   Then a collectioncatalog with the title 'My CollectionCatalog' has been created


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add collectioncatalog form
  Go To  ${PLONE_URL}/++add++dcat_collection_catalog

a collectioncatalog 'My CollectionCatalog'
  Create content  type=dcat_collectioncatalog  id=my-collectioncatalog  title=My CollectionCatalog

a publisher 'Test-Publisher'
  Go To  ${PLONE_URL}/publishers/++add++foaf_agent
  I type 'Test-Publisher' into the name field
  I submit the form

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.en  ${title}

I type '${title}' into the name field
  Input Text  form.widgets.foaf_name.en  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.en  ${description}

I submit the form
  Click Button  Save

I go to the collectioncatalog view
  Go To  ${PLONE_URL}/my-collectioncatalog
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a collectioncatalog with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the collectioncatalog title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
