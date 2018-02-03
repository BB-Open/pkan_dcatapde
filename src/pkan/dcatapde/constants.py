# -*- coding: utf-8 -*-
"""Constants for easier access."""

# content types
CT_DCAT_CATALOG = 'dcat_catalog'
CT_FOAF_AGENT = 'foaf_agent'
CT_DCT_LICENSE_DOCUMENT = 'dct_licensedocument'
CT_DCT_MEDIATYPEOREXTENT = 'dct_mediatypeorextent'
CT_DCAT_DISTRIBUTION = 'dcat_distribution'
CT_DCAT_DATASET = 'dcat_dataset'
CT_HARVESTER_FOLDER = 'harvesterfolder'
CT_HARVESTER = 'harvester'
CT_HARVESTER_FIELD_CONFIG = 'harvester_field_config'
CT_SCOS_CONCEPTSCHEME = 'scos_conceptscheme'

# folder CTs to contain CTs
CT_LICENSE_FOLDER = 'LicenseFolder'
CT_AGENT_FOLDER = 'AgentFolder'
CT_FORMATS_FOLDER = 'FormatFolder'
CT_MEDIATYPE_FOLDER = 'MediaTypeFolder'
CT_CONCEPTSCHEME_FOLDER = 'ConceptSchemeFolder'


DCAT_CTs = [
    CT_DCAT_CATALOG,
    CT_DCAT_DATASET,
    CT_DCAT_DISTRIBUTION,
    CT_FOAF_AGENT,
    CT_DCT_LICENSE_DOCUMENT,
    CT_DCT_MEDIATYPEOREXTENT,
    CT_SCOS_CONCEPTSCHEME,
]


# HTML filled with error information from harvesting dry_run
ERROR_HTML_LINE = '<p>Found error {error} on field {field}</p>'


#: Default folder names (relative to portal root)
FOLDER_LICENSES = 'licenses'
FOLDER_AGENTS = 'agents'
FOLDER_FORMATS = 'formats'
FOLDER_MEDIATYPES = 'mediatypes'
FOLDER_CONCEPTS = 'concepts'

# Location of vocabulary sources

VOCAB_SOURCES = {
    CT_DCT_LICENSE_DOCUMENT: 'http://www.dcat-ap.de/def/licenses/1_0.rdf',
}


#: All folders to be created at installation of the module
MANDATORY_FOLDERS = {
    FOLDER_LICENSES: CT_LICENSE_FOLDER,
    FOLDER_AGENTS: CT_AGENT_FOLDER,
    FOLDER_FORMATS: CT_FORMATS_FOLDER,
    FOLDER_MEDIATYPES: CT_MEDIATYPE_FOLDER,
    FOLDER_CONCEPTS: CT_CONCEPTSCHEME_FOLDER,
}

HARVESTER_FIELD_CONFIG_TITLE = 'Field Config'
HARVESTER_FIELD_CONFIG_ID = 'field_config'

HARVESTER_FOLDER_TITLE = 'Harvester Folder'
HARVESTER_FOLDER_ID = 'harvester_folder'
