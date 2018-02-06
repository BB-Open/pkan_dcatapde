*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to change the base settings
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@pkan-controlpanel-base

    Page should contain element  id=content
    Capture and crop page screenshot
    ...  settings_base.png
    ...  id=content


Show how to change the folder settings
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@pkan-controlpanel-folders

    Page should contain element  id=content
    Capture and crop page screenshot
    ...  settings_folders.png
    ...  id=content

    Page should contain element  id=formfield-form-widgets-folder_agents
    Capture and crop page screenshot
    ...  settings_folders-folder_agents.png
    ...  id=formfield-form-widgets-folder_agents

    Page should contain element  id=formfield-form-widgets-folder_formats
    Capture and crop page screenshot
    ...  settings_folders-folder_formats.png
    ...  id=formfield-form-widgets-folder_formats

    Page should contain element  id=formfield-form-widgets-folder_licenses
    Capture and crop page screenshot
    ...  settings_folders-folder_licenses.png
    ...  id=formfield-form-widgets-folder_licenses

    Page should contain element  id=formfield-form-widgets-folder_locations
    Capture and crop page screenshot
    ...  settings_folders-folder_locations.png
    ...  id=formfield-form-widgets-folder_locations

    Page should contain element  id=formfield-form-widgets-folder_publishers
    Capture and crop page screenshot
    ...  settings_folders-folder_publishers.png
    ...  id=formfield-form-widgets-folder_publishers

    Page should contain element  id=formfield-form-widgets-folder_standards
    Capture and crop page screenshot
    ...  settings_folders-folder_standards.png
    ...  id=formfield-form-widgets-folder_standards
