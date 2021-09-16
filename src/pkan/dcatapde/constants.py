# -*- coding: utf-8 -*-
"""Constants for easier access."""

from pkan.dcatapde import _


# Content Types
CT_DCAT_CATALOG = 'dcat_catalog'
CT_DCAT_COLLECTION_CATALOG = 'dcat_collection_catalog'
CT_DCAT_DATASET = 'dcat_dataset'
CT_DCAT_DISTRIBUTION = 'dcat_distribution'
CT_DCT_LICENSEDOCUMENT = 'dct_licensedocument'
CT_DCT_LANGUAGE = 'dct_language'
CT_DCT_LOCATION = 'dct_location'
CT_DCT_MEDIATYPEOREXTENT = 'dct_mediatypeorextent'
CT_DCT_RIGHTSSTATEMENT = 'dct_rightsstatement'
CT_DCT_STANDARD = 'dct_standard'
CT_FOAF_AGENT = 'foaf_agent'
CT_HARVESTER = 'harvester'
CT_HARVESTER_FOLDER = 'harvesterfolder'
CT_TRANSFER_FOLDER = 'transferfolder'
CT_TRANSFER = 'transfer'
CT_RDFS_LITERAL = 'rdfs_literal'
CT_SKOS_CONCEPT = 'skos_concept'
CT_SKOS_CONCEPTSCHEME = 'skos_conceptscheme'
CT_VCARD_KIND = 'vcard_kind'
CT_PLONE_SITE = 'Plone Site'
CT_ANY = 'any'

# Folder CTs to contain CTs
CT_AGENT_FOLDER = 'AgentFolder'
CT_CONCEPT_FOLDER = 'ConceptFolder'
CT_CONCEPTSCHEME_FOLDER = 'ConceptSchemeFolder'
CT_VCARDKIND_FOLDER = 'VcardKindFolder'
CT_FORMAT_FOLDER = 'FormatFolder'
CT_LICENSE_FOLDER = 'LicenseFolder'
CT_LOCATION_FOLDER = 'LocationFolder'
CT_MEDIATYPE_FOLDER = 'MediaTypeFolder'
CT_RIGHTS_FOLDER = 'RightsFolder'
CT_STANDARDS_FOLDER = 'StandardsFolder'
CT_LANGUAGE_FOLDER = 'LanguageFolder'

CT_PUBLISHER_CARD = 'PublisherCard'

# list of DCAT CTs
DCAT_CTs = [
    CT_DCAT_CATALOG,
    CT_DCAT_COLLECTION_CATALOG,
    CT_DCAT_DATASET,
    CT_DCAT_DISTRIBUTION,
    CT_FOAF_AGENT,
    CT_DCT_LICENSEDOCUMENT,
    CT_DCT_MEDIATYPEOREXTENT,
    CT_DCT_RIGHTSSTATEMENT,
    CT_DCT_STANDARD,
    CT_SKOS_CONCEPT,
    CT_SKOS_CONCEPTSCHEME,
    CT_DCT_LANGUAGE,
    CT_VCARD_KIND,
]

# list of DCAT Top nodes
DCAT_TOP_NODES = [
    CT_DCAT_CATALOG,
    CT_DCAT_DATASET,
    CT_ANY,
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

#: Default folder shortname for vcard kinds.
FOLDER_VCARD_KIND = 'vcardkinds'

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
FOLDER_RIGHTS = 'rightsfolder'

#: Default folder shortname for languages
FOLDER_LANGUAGES = 'languages'

# Location of vocabulary sources
# todo move to registry
VOCAB_SOURCES = {
    CT_DCT_LICENSEDOCUMENT: 'http://www.dcat-ap.de/def/licenses/20180514.rdf',
    CT_SKOS_CONCEPT: {
        'http://publications.europa.eu/resource/authority/data-theme/AGRI': 'fa-tree',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/ECON': 'fa-shopping-cart',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/EDUC': 'fa-laptop',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/ENER': 'fa-battery-full',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/ENVI': 'fa-leaf',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/HEAL': 'fa-stethoscope',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/INTR': 'fa-globe',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/JUST': 'fa-balance-scale',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/SOCI': 'fa-github',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/GOVE': 'fa-inbox',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/REGI': 'fa-building',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/TECH': 'fa-microchip',  # noqa E501
        'http://publications.europa.eu/resource/authority/data-theme/TRAN': 'fa-train',  # noqa E501
    },

    CT_DCT_LANGUAGE: 'data/languages.rdf',
}

#: All folders to be created at installation of the module
MANDATORY_FOLDERS = {
    FOLDER_AGENTS: CT_AGENT_FOLDER,
    FOLDER_CONCEPTS: CT_CONCEPT_FOLDER,
    FOLDER_CONCEPTSCHEMES: CT_CONCEPTSCHEME_FOLDER,
    FOLDER_VCARD_KIND: CT_VCARDKIND_FOLDER,
    FOLDER_FORMATS: CT_FORMAT_FOLDER,
    FOLDER_LICENSES: CT_LICENSE_FOLDER,
    FOLDER_LOCATIONS: CT_LOCATION_FOLDER,
    FOLDER_MEDIATYPES: CT_MEDIATYPE_FOLDER,
    FOLDER_PUBLISHERS: CT_AGENT_FOLDER,
    FOLDER_RIGHTS: CT_RIGHTS_FOLDER,
    FOLDER_STANDARDS: CT_STANDARDS_FOLDER,
    FOLDER_LANGUAGES: CT_LANGUAGE_FOLDER,
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

RDF_REPO_TYPE = 'native-rdfs'

# Limit for preview output, if output is longer it will be shortened
MAX_QUERY_PREVIEW_LENGTH = 1000

FIELD_BLACKLIST = [
    'exclude_from_nav',
    'changeNode',
]

# Harvester Annotation Key to store harvester_entity
HARVESTER_ENTITY_KEY = 'pkan.dcatapde.harvesting.entity_mapping'
HARVESTER_DEXTERITY_KEY = 'pkan.dcatapde.harvesting.dexterity_mapping'
HARVESTER_DEFAULT_KEY = 'pkan.dcatapde.harvesting.default_mapping'

# Import Views
# mapping Folder from MANDATORY_FOLDERS to View name
IMPORT_URLS = {
    FOLDER_LICENSES: 'update_licenses',
    FOLDER_CONCEPTS: 'update_themes',
    FOLDER_LANGUAGES: 'update_languages',
}

# Fieldsets that should be ordered at the and of display views, even after
# folder contents
FIELDSET_ORDER_AT_END = ['internal_info']

# Time Out for language cache in seconds
LANGUAGE_CACHE_TIMEOUT = 300

# ROLES
PROVIDER_CHIEF_EDITOR_ROLE = 'ProviderChiefEditor'
PROVIDER_DATA_EDITOR_ROLE = 'ProviderDataEditor'
PROVIDER_ADMIN_ROLE = 'ProviderAdmin'
LANDING_PAGE_VIEW = 'landing_page'
ADMIN_LANDING_PAGE = 'admin_landing_page'

# STATES
ACTIVE_STATE = 'active'
DEACTIVE_STATE = 'deactive'
PKAN_STATE_NAME = 'pkan_state'
PRVIDER_DATA_EDITOR_PERM = 'pkan.dcatapde.ProviderDataEditor'
PROVIDER_ADMIN_PERM = 'pkan.dcatapde.ProviderAdmin'
PROVIDER_CHIEF_EDITOR_PERM = 'pkan.dcatapde.ProviderChiefEditor'

CT_DCAT_DISTRIBUTION_TRANS = _(u'dcat_distribution')
VOLUMN_TYPES = {
    _(u'File'): ['file', 'size'],
    _(u'Image'): ['image', 'size'],
    CT_DCAT_DISTRIBUTION_TRANS: ['local_file', '_size'],
}

SIZE_UNIT = 'MB'
SIZE_FACTOR = 1024 ** 2
SIZE_ROUND = 2

IMPRESSUM = 'Impressum'
HARVEST_TRIPELSTORE = 'Tripelstore'

# RDF4J
RDF4J_BASE = 'http://192.168.122.193:8080/rdf4j-server/'

ADMIN_USER = 'admin'
ADMIN_PASS = 'pw1'

EDITOR_USER = 'editor'
EDITOR_PASS = 'pw2'

VIEWER_USER = 'viewer'
VIEWER_PASS = 'pw3'
