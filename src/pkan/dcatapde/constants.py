# -*- coding: utf-8 -*-
"""Constants for easier access."""

CT_Catalog = 'catalog'
CT_Foafagent = 'foafagent'
CT_DCT_LICENSE_DOCUMENT = 'dct_licensedocument'
CT_DctMediatypeorextent = 'dct_mediatypeorextent'
CT_Distribution = 'distribution'
CT_Dataset = 'dataset'
CT_HarvesterFolder = 'harvesterfolder'
CT_Harvester = 'harvester'
CT_HarvesterFieldConfig = 'harvester_field_config'


DCAT_CTs = [
    CT_Catalog,
    CT_Dataset,
    CT_Distribution,
]


# HTML filled with error information from harvesting dry_run
ERROR_HTML_LINE = '<p>Found error {error} on field {field}</p>'


#: Default folder for licenses.
FOLDER_LICENSES = 'licenses'

HARVESTER_FIELD_CONFIG_TITLE = 'Field Config'
HARVESTER_FIELD_CONFIG_ID = 'field_config'


HARVESTER_FOLDER_TITLE = 'Harvester Folder'
HARVESTER_FOLDER_ID = 'harvester_folder'
