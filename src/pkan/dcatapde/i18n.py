# -*- coding: utf-8 -*-
"""I18N message id's."""

from pkan.dcatapde import _
from pkan.dcatapde import constants

BUTTON_IMPORT_DCT_LICENSEDOCUMENT = _(u'Import DCT:LicenseDocument')
BUTTON_IMPORT_SKOS_CONCEPT = _(u'Import SKOS:Concept')
BUTTON_IMPORT_LANGUAGES = _(u'Import Lanuages')

PERMISSION_DENIED = _(u'Permission Denied')
DEPRECATED = _(u':Deprecated')

FIELDSET_AGENTS = _(u'Agents')
FIELDSET_DETAILS = _(u'Dates, Geo, etc')
FIELDSET_RELATIONS = _(u'Relations')
FIELDSET_INTERNAL_INFO = _(u'Object Identifier')

IDENTIFIER_DESCRIPTION = _(u'Default will be Plone-URL.')

HELP_SELECT_FIELD = u'If only an ID is displayed, the value is not released and must be replaced.'

HELP_BASE_OBJECT = _(
    u'Here you may chose the location where to the datasets will be '
    u'imported. If the incoming data has no catalog, choose a '
    u'catalog object.'
    u'By default incoming catalogues are place in the harvester. ',
)
HELP_DACT_MEDIATYPE = _(
    u'Select a media type from the list of available media types. ' + HELP_SELECT_FIELD,
    # or create '
    # # u'a new one by using the "add" button below.',
)
HELP_DACTDE_MAINTAINER = _(
    u'Select a maintainer from the list of available maintainers. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DACTDE_ORIGINATOR = _(
    u'Select an originator from the list of available originators. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_ACCESSRIGHTS = _(
    u'Select a access right from the list of available access rights. ' + HELP_SELECT_FIELD,
)
HELP_DCT_CONFORMSTO = _(
    u'Select a standard from the list of available standards. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_CONTRIBUTOR = _(
    u'Select a contributor from the list of available contributors. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_CREATOR = _(
    u'Select a creator from the list of available creators. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_FORMAT = _(
    u'Select a format from the list of available formats. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_HASPART = _(
    u'Link to an existing catalog. ' + HELP_SELECT_FIELD,
    # or create a new one by using the '
    # u'"add" button below.',
)
HELP_DCT_ISPARTOF = _(
    u'Link to an existing parent catalog. ' + HELP_SELECT_FIELD,
    # or create a new one by using the '
    # u'"add" button below.',
)
HELP_DCT_LICENSE = _(
    u'Select a license from the list of available licenses. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_PUBLISHER = _(
    u'Select a publisher from the list of available publishers. ' + HELP_SELECT_FIELD,
    # or create '
    # u'a new one by using the "add" button below.',
)
HELP_DCT_RIGHTS = _(
    u'Select a rights statement from the list of available statements. ' + HELP_SELECT_FIELD,
    # or '
    # u'create a new one by using the "add" button below.',
)
HELP_DCT_SPATIAL = _(
    u'Select a location from the list of available locations. ' + HELP_SELECT_FIELD,
    # or '
    # u'create a new one by using the "add" button below.',
)
HELP_DCT_THEMETAXONOMY = _(
    u'Select a theme taxonomy from the list of available taxonomies. ' + HELP_SELECT_FIELD,
    # or '
    # u'create a new one by using the "add" button below.',
)
HELP_FOLDER_AGENTS = _(
    u'Please enter the folder containing all agents, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_AGENTS),
    },
)
HELP_FOLDER_FORMATS = _(
    u'Please enter the folder containing all formats, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_FORMATS),
    },
)
HELP_FOLDER_LICENSES = _(
    u'Please enter the folder containing all licenses, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_LICENSES),
    },
)
HELP_FOLDER_LOCATIONS = _(
    u'Please enter the folder containing all locations, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_LOCATIONS),
    },
)
HELP_FOLDER_PUBLISHERS = _(
    u'Please enter the folder containing all publishers, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_PUBLISHERS),
    },
)
HELP_FOLDER_STANDARDS = _(
    u'Please enter the folder containing all standards, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_STANDARDS),
    },
)
HELP_FOLDER_LANGUAGES = _(
    u'Please enter the folder containing all languages, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_LANGUAGES),
    },
)
HELP_RDFS_ISDEFINEDBY = _(u'The URI describing this concept')
HELP_SKOS_CONCEPT = _(u'Select some SKOS Concepts. ' + HELP_SELECT_FIELD)
HELP_VCARD_KIND = _(u'Select a contact information. ' + HELP_SELECT_FIELD)
HELP_SETTINGS_BASE = _(u'Manage base settings for PKAN.')
HELP_SETTINGS_FOLDERS = _(u'Manage folder settings for PKAN.')
HELP_SETTINGS_IMPORTS = _(u'Manage import settings for PKAN.')
HELP_SETTINGS_IMPORTS_DCT_LICENSEDOCUMENT = _(
    u'Define the import sources for DCT:LicenseDocument objects.',
)
HELP_SETTINGS_IMPORTS_SKOS_CONCEPT = _(
    u'Define the import sources for SKOS:Concept objects.',
)
HELP_SETTINGS_IMPORTS_DCT_LANGUAGE = _(
    u'Define the import sources for DCT:Language objects.',
)

HELP_SKOS_INSCHEME = _(u'URI to the concept scheme')
HELP_REHARVESTING_PERIOD = _(
    u'Decide how often the harvester should be reharvested automatically. '
    u'Leave empty for no reharvesting. Shortest intervall is one day. '
    u'Period is parsed using pytimeparse. '
    u'Read about on https://pypi.org/project/pytimeparse/',
)
HELP_FOAF_DEPICTION = _(u'Visual representation of the category')

LABEL_ADMS_IDENTIFIER = _(u'Local identifier')
LABEL_ADMS_VERSIONNOTES = _(u'Version Notes')
LABEL_BASE_OBJECT = _(u'Base Object')
LABEL_DCAT_ACCESSURL = _(u'Access URL')
LABEL_DCAT_BYTESIZE = _(u'Byte size')
LABEL_DCAT_CATALOG = _(u'Catalog')
LABEL_DCAT_COLLECTION_CATALOG = _(u'Collection Catalog')
LABEL_DCAT_DATASET = _(u'Dataset')
LABEL_DCAT_DOWNLOADURL = _(u'Download URL')
LABEL_LOCAL_FILE = _(u'Local file')
LABEL_DCAT_DISTRIBUTION = _(u'Distribution')
LABEL_DCAT_MEDIATYPE = _(u'Media type')
LABEL_DCATDE_CONTRIBUTORID = _(u'Contributor ID')
LABEL_DCATDE_GEOCODINGTEXT = _(u'Geocoding text')
LABEL_DCATDE_LEGALBASISTEXT = _(u'Legal basis text')
LABEL_DCATDE_LICENSEATTRIBUTIONBYTEXT = _(u'Licence attribution by text')
LABEL_DCATDE_MAINTAINER = _(u'Maintainer')
LABEL_DCATDE_POLITICALGEOCODINGLEVELURI = _(u'PoliticalGeocodingLevelURI')
LABEL_DCATDE_POLITICALGEOCODINGURI = _(u'PoliticalGeocodingURI')
LABEL_DCATDE_ORIGINATOR = _(u'Originator')
LABEL_DCT_ACCESSRIGHTS = _(u'Access Rights')
LABEL_DCT_CONFORMSTO = _(u'Conform to Standard')
LABEL_DCT_CONTRIBUTOR = _(u'Contributor')
LABEL_DCT_CREATOR = _(u'Creator')
LABEL_DCT_DESCRIPTION = _(u'Description')
LABEL_DCT_FORMAT = _(u'Format')
LABEL_DCT_HASPART = _(u'Parts')
LABEL_DCT_IDENTIFIER = _(u'Primary Identifier')
LABEL_DCT_ISPARTOF = _(u'Parent Catalog')
LABEL_DCT_ISSUED = _(u'Issued')
LABEL_DCT_LANGUAGE = _(u'Languages')
LABEL_DCT_LICENSE = _(u'License')
LABEL_DCT_LICENSEDOCUMENT = _(u'License Document')
LABEL_DCT_LOCATION = _(u'Location')
LABEL_DCT_MODIFIED = _(u'Modified')
LABEL_DCT_MEDIATYPEOREXTENT = _(u'Mediatype')
LABEL_DCT_PUBLISHER = _(u'Publisher')
LABEL_DCT_RIGHTS = _(u'Rights')
LABEL_DCT_RIGHTSSTATEMENT = _(u'Rights statement')
LABEL_DCT_SPATIAL = _(u'Spatial relevance')
LABEL_DCT_STANDARD = _(u'Standard')
LABEL_DCT_THEMETAXONOMY = _(u'Theme Taxonomy')
LABEL_DCT_TITLE = _(u'Title')
LABEL_FOAF_AGENT = _(u'Agent')
LABEL_FOAF_HOMEPAGE = _(u'Homepage')
LABEL_DCAT_LANDINGPAGE = _(u'Landing page')
LABEL_FOAF_PAGE = _(u'Page')
LABEL_FOLDER_AGENTS = _(u'Folder containing agents')
LABEL_FOLDER_FORMATS = _(u'Folder containing formats')
LABEL_FOLDER_LICENSES = _(u'Folder containing licenses')
LABEL_FOLDER_LOCATIONS = _(u'Folder containing locations')
LABEL_FOLDER_LANGUAGES = _(u'Folder containing languages')
LABEL_FOLDER_PUBLISHERS = _(u'Folder containing publishers')
LABEL_FOLDER_STANDARDS = _(u'Folder containing standards')
LABEL_HARVESTER = _(u'Harvester')
LABEL_HARVESTER_FOLDER = _(u'Harvester folder')
LABEL_OWL_VERSIONINFO = _(u'Version info')
LABEL_RDF_ABOUT = _(u'Access URI')
LABEL_RDFS_LITERAL = _(u'Literal')
LABEL_RDFS_ISDEFINEDBY = _(u'Definition URI')
LABEL_SKOS_CONCEPT = _(u'SCOS concept')
LABEL_SKOS_CONCEPTSCHEME = _(u'SCOS concept scheme')
LABEL_VCARD_KIND = _(u'Vcard Kind')
LABEL_SETTINGS_BASE = _(u'PKAN Base Settings')
LABEL_SETTINGS_FOLDERS = _(u'PKAN Folder Settings')
LABEL_SETTINGS_IMPORTS = _(u'PKAN Import Settings')
LABEL_SETTINGS_IMPORTS_DCT_LICENSEDOCUMENT = _('DCT:LicenseDocument Sources')
LABEL_SETTINGS_IMPORTS_SKOS_CONCEPT = _('SKOS:Concept Sources')
LABEL_SETTINGS_IMPORTS_DCT_LANGUAGE = _('DCT:Language Sources')
LABEL_SKOS_INSCHEME = _(u'Concept scheme URI')
LABEL_URL = _(u'URL')

STATUS_REGISTRY_UPDATED = _(
    u'Registry has been updated. Please reload this page.',
)

# Content type labels
CT_LABELS = {
    constants.CT_DCAT_CATALOG: LABEL_DCAT_CATALOG,
    constants.CT_DCAT_COLLECTION_CATALOG: LABEL_DCAT_COLLECTION_CATALOG,
    constants.CT_DCAT_DATASET: LABEL_DCAT_DATASET,
    constants.CT_DCAT_DISTRIBUTION: LABEL_DCAT_DISTRIBUTION,
    constants.CT_DCT_LICENSEDOCUMENT: LABEL_DCT_LICENSEDOCUMENT,
    constants.CT_DCT_LOCATION: LABEL_DCT_LOCATION,
    constants.CT_DCT_LANGUAGE: LABEL_DCT_LANGUAGE,
    constants.CT_DCT_MEDIATYPEOREXTENT: LABEL_DCT_MEDIATYPEOREXTENT,
    constants.CT_DCT_RIGHTSSTATEMENT: LABEL_DCT_RIGHTSSTATEMENT,
    constants.CT_DCT_STANDARD: LABEL_DCT_STANDARD,
    constants.CT_FOAF_AGENT: LABEL_FOAF_AGENT,
    constants.CT_HARVESTER: LABEL_HARVESTER,
    constants.CT_HARVESTER_FOLDER: LABEL_HARVESTER_FOLDER,
    constants.CT_RDFS_LITERAL: LABEL_RDFS_LITERAL,
    constants.CT_SKOS_CONCEPT: LABEL_SKOS_CONCEPT,
    constants.CT_SKOS_CONCEPTSCHEME: LABEL_SKOS_CONCEPTSCHEME,
    constants.CT_VCARD_KIND: LABEL_VCARD_KIND,
}

# Data Volumn
LABEL_SUM = _(u'Sum')
VOLUMN_RESULT_STRING = _(u'${label}: Count: ${count}; Size: ${size} ${unit}')
