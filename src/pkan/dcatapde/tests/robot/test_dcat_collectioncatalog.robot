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

Scenario: As a site admin I can filter datasets
  Given a logged-in site administrator
    and a publisher 'Test-Publisher'
    and a catalog 'My Catalog'
    and a dataset 'My Dataset'
    and an add collectioncatalog form
   When I type 'My CollectionCatalog' into the title field
    and I type 'A description' into the description field
    and I select 'Test-Publisher' from an AJAX select widget with id 'formfield-form-widgets-dct_publisher'
    and I set the collection's type criterion to  DCAT:Dataset
    and I submit the form
  Then a collectioncatalog with the title 'My CollectionCatalog' has been created
    and I can see the item title 'My Dataset'

Scenario: As a site admin I can filter catalogs
  Given a logged-in site administrator
    and a publisher 'Test-Publisher'
    and a catalog 'My Catalog'
    and an add collectioncatalog form
   When I type 'My CollectionCatalog' into the title field
    and I type 'A description' into the description field
    and I select 'Test-Publisher' from an AJAX select widget with id 'formfield-form-widgets-dct_publisher'
    and I set the collection's type criterion to  DCAT:Catalog
    and I submit the form
  Then a collectioncatalog with the title 'My CollectionCatalog' has been created
    and I can see the item title 'My Catalog'


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

a catalog 'My Catalog'
  Go To  ${PLONE_URL}/++add++dcat_catalog
  I type 'My Catalog' into the title field
  I type 'A description' into the description field
  I select 'Test-Publisher' from an AJAX select widget with id 'formfield-form-widgets-dct_publisher'
  I submit the form

a dataset 'My Dataset'
  Go To  ${PLONE_URL}/dcat_catalog/++add++dcat_dataset
  I type 'My Dataset' into the title field
  I type 'A description' into the description field
  I type 'testid' into the dcatde_contributorID field
  I submit the form


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  form.widgets.dct_title.eng  ${title}

I type '${title}' into the name field
  Input Text  form.widgets.foaf_name.eng  ${title}

I type '${description}' into the description field
  Input Text  form.widgets.dct_description.eng  ${description}

I submit the form
  Click Button  Save

I go to the collectioncatalog view
  Go To  ${PLONE_URL}/my-collectioncatalog
  Wait until page contains  Site Map

I set the collection's type criterion to
    [Arguments]  ${criterion}

    I set the criteria index in row 1 to the option 'Type'
    I set the criteria operator in row 1 to the option 'Any'
    I set the criteria value in row 1 to the options '${criterion}'

I type '${dcatde_contributorID}' into the dcatde_contributorID field
  Input Text  form.widgets.dcatde_contributorID.eng  ${dcatde_contributorID}

# --- THEN -------------------------------------------------------------------

a collectioncatalog with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
#  Page should contain  Item created

I can see the collectioncatalog title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

I can see the item title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
