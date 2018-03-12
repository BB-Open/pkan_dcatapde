# -*- coding: utf-8 -*-
"""Constants for easier access."""

# Content Types
CT_DCAT_CATALOG = 'dcat_catalog'
CT_DCAT_DATASET = 'dcat_dataset'
CT_DCAT_DISTRIBUTION = 'dcat_distribution'
CT_DCT_LICENSEDOCUMENT = 'dct_licensedocument'
CT_DCT_LOCATION = 'dct_location'
CT_DCT_MEDIATYPEOREXTENT = 'dct_mediatypeorextent'
CT_DCT_RIGHTSSTATEMENT = 'dct_rightsstatement'
CT_DCT_STANDARD = 'dct_standard'
CT_FOAF_AGENT = 'foaf_agent'
CT_HARVESTER = 'harvester'
CT_HARVESTER_FOLDER = 'harvesterfolder'
CT_RDF_LITERAL = 'rdf_literal'
CT_SKOS_CONCEPT = 'skos_concept'
CT_SKOS_CONCEPTSCHEME = 'skos_conceptscheme'
CT_PLONE_SITE = 'Plone Site'

# Folder CTs to contain CTs
CT_AGENT_FOLDER = 'AgentFolder'
CT_CONCEPT_FOLDER = 'ConceptFolder'
CT_CONCEPTSCHEME_FOLDER = 'ConceptSchemeFolder'
CT_FORMAT_FOLDER = 'FormatFolder'
CT_LICENSE_FOLDER = 'LicenseFolder'
CT_LOCATION_FOLDER = 'LocationFolder'
CT_MEDIATYPE_FOLDER = 'MediaTypeFolder'
CT_RIGHTS_FOLDER = 'RightsFolder'
CT_STANDARDS_FOLDER = 'StandardsFolder'

# list of DCAT CTs
DCAT_CTs = [
    CT_DCAT_CATALOG,
    CT_DCAT_DATASET,
    CT_DCAT_DISTRIBUTION,
    CT_FOAF_AGENT,
    CT_DCT_LICENSEDOCUMENT,
    CT_DCT_MEDIATYPEOREXTENT,
    CT_DCT_RIGHTSSTATEMENT,
    CT_DCT_STANDARD,
    CT_SKOS_CONCEPT,
    CT_SKOS_CONCEPTSCHEME,
]

# list of DCAT Top nodes
DCAT_TOP_NODES = [
    CT_DCAT_CATALOG,
    CT_DCAT_DATASET,
]

# DCAT predicates
DP_DCAT_DATASET = 'dcat:Dataset'


# HTML filled with error information from harvesting dry_run
ERROR_HTML_LINE = '<p>Found error {error} on field {field}</p>'

#: Default folder shortname for agents.
FOLDER_AGENTS = 'agents'

#: Default folder shortname for concepts.
FOLDER_CONCEPTS = 'concepts'

#: Default folder shortname for conceptschemes.
FOLDER_CONCEPTSCHEMES = 'conceptschemes'

#: Default folder shortname for formats.
FOLDER_FORMATS = 'formats'

#: Default folder shortname for licenses.
FOLDER_LICENSES = 'licenses'

#: Default folder shortname for locations.
FOLDER_LOCATIONS = 'locations'

#: Default folder shortname for mediatypes.
FOLDER_MEDIATYPES = 'mediatypes'

#: Default folder shortname for publishers.
FOLDER_PUBLISHERS = 'publishers'

#: Default folder shortname for standards.
FOLDER_STANDARDS = 'standards'

#: Default folder shortname for standards.
FOLDER_RIGHTS = 'rightsf'


# Location of vocabulary sources
VOCAB_SOURCES = {
    CT_DCT_LICENSEDOCUMENT: 'http://www.dcat-ap.de/def/licenses/1_0.rdf',
    CT_SKOS_CONCEPT: 'http://publications.europa.eu/mdr/resource/authority'
                     '/data-theme/skos/data-theme-skos.rdf',
}

#: All folders to be created at installation of the module
MANDATORY_FOLDERS = {
    FOLDER_AGENTS: CT_AGENT_FOLDER,
    FOLDER_CONCEPTS: CT_CONCEPT_FOLDER,
    FOLDER_CONCEPTSCHEMES: CT_CONCEPTSCHEME_FOLDER,
    FOLDER_FORMATS: CT_FORMAT_FOLDER,
    FOLDER_LICENSES: CT_LICENSE_FOLDER,
    FOLDER_LOCATIONS: CT_LOCATION_FOLDER,
    FOLDER_MEDIATYPES: CT_MEDIATYPE_FOLDER,
    FOLDER_PUBLISHERS: CT_AGENT_FOLDER,
    FOLDER_RIGHTS: CT_RIGHTS_FOLDER,
    FOLDER_STANDARDS: CT_STANDARDS_FOLDER,
}

HARVESTER_FOLDER_TITLE = 'Harvester Folder'
HARVESTER_FOLDER_ID = 'harvester_folder'

# RDF formats

# RDF format keys for vocabularies
RDF_FORMAT_JSONLD = 'JSONLD'
RDF_FORMAT_TURTLE = 'TURTLE'
RDF_FORMAT_XML = 'XML'

#
RDF_FORMAT_METADATA = {
    RDF_FORMAT_JSONLD: {
        'serialize_as': 'json-ld',
        'mime_type': 'application/ld+json; charset=utf-8',
    },
    RDF_FORMAT_TURTLE: {
        'serialize_as': 'turtle',
        'mime_type': 'text/turtle; charset=utf-8',
    },
    RDF_FORMAT_XML: {
        # todo: pretty-xml no parser registered
        'serialize_as': 'application/rdf+xml',
        'mime_type': 'application/rdf+xml; charset=utf-8',
    },
}

# Limit for preview output, if output is longer it will be shortened
MAX_QUERY_PREVIEW_LENGTH = 1000

FIELD_BLACKLIST = [
    'exclude_from_nav',
]

# Harvester Annotation Key to store harvester_entity
HARVESTER_ENTITY_KEY = 'pkan.dcatapde.harvesting.entity_mapping'
HARVESTER_DEXTERITY_KEY = 'pkan.dcatapde.harvesting.dexterity_mapping'
HARVESTER_DEFAULT_KEY = 'pkan.dcatapde.harvesting.default_mapping'
