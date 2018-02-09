# -*- coding: utf-8 -*-
"""I18N message id's."""

from pkan.dcatapde import _
from pkan.dcatapde import constants


BUTTON_IMPORT_DCT_LICENSEDOCUMENT = _(u'Import DCT:LicenseDocument')
BUTTON_IMPORT_SKOS_CONCEPT = _(u'Import SKOS:Concept')

FIELDSET_AGENTS = _(u'Agents')
FIELDSET_DETAILS = _(u'Dates, Geo, etc')
FIELDSET_RELATIONS = _(u'Relations')


HELP_DACT_MEDIATYPE = _(
    u'Select a media type from the list of available media types or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DACTDE_MAINTAINER = _(
    u'Select a maintainer from the list of available maintainers or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DACTDE_ORIGINATOR = _(
    u'Select an originator from the list of available originators or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_CONFORMSTO = _(
    u'Select a standard from the list of available standards or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_CONTRIBUTOR = _(
    u'Select a contributor from the list of available contributors or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_CREATOR = _(
    u'Select a creator from the list of available creators or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_FORMAT = _(
    u'Select a format from the list of available formats or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_HASPART = _(
    u'Link to an existing catalog or or create a new one by using the '
    u'\'add\' button below.',
)
HELP_DCT_ISPARTOF = _(
    u'Link to an existing parent catalog or or create a new one by using the '
    u'\'add\' button below.',
)
HELP_DCT_LICENSE = _(
    u'Select a license from the list of available licenses or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_PUBLISHER = _(
    u'Select a publisher from the list of available publishers or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_RIGHTS = _(
    u'Select a rights statement from the list of available statements or '
    u'create a new one by using the \'add\' button below.',
)
HELP_DCT_SPATIAL = _(
    u'Select a location from the list of available locations or '
    u'create a new one by using the \'add\' button below.',
)
HELP_DCT_THEMETAXONOMY = _(
    u'Select a theme taxonomy from the list of available taxonomies or '
    u'create a new one by using the \'add\' button below.',
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
HELP_RDFS_ISDEFINEDBY = _(u'The URI describing this concept')
HELP_SETTINGS_BASE = _(u'Manage base settings for PKAN.')
HELP_SETTINGS_FOLDERS = _(u'Manage folder settings for PKAN.')
HELP_SETTINGS_IMPORTS = _(u'Manage import settings for PKAN.')
HELP_SETTINGS_IMPORTS_DCT_LICENSEDOCUMENT = _(
    u'Define the import sources for DCT:LicenseDocument objects.',
)
HELP_SETTINGS_IMPORTS_SKOS_CONCEPT = _(
    u'Define the import sources for SKOS:Concept objects.',
)
HELP_SKOS_INSCHEME = _(u'URI to the concept scheme')


LABEL_ADMS_IDENTIFIER = _(u'Identifier')
LABEL_ADMS_VERSIONNOTES = _(u'Version Notes')
LABEL_DCAT_ACCESSURL = _(u'Access URL')
LABEL_DCAT_BYTESIZE = _(u'Byte size')
LABEL_DCAT_DOWNLOADURL = _(u'Download URL')
LABEL_DCAT_MEDIATYPE = _(u'Media type')
LABEL_DCATDE_CONTRIBUTORID = _(u'Contributor ID')
LABEL_DCATDE_GEOCODINGTEXT = _(u'Geocoding text')
LABEL_DCATDE_LEGALBASISTEXT = _(u'Legal basis text')
LABEL_DCATDE_LICENSEATTRIBUTIONBYTEXT = _(u'Licence attribution by text')
LABEL_DCATDE_MAINTAINER = _(u'Maintainer')
LABEL_DCATDE_PLANNED_AVAILABLITY = _(u'Planed availability')
LABEL_DCATDE_POLITICALGEOCODINGLEVELURI = _(u'PoliticalGeocodingLevelURI')
LABEL_DCATDE_POLITICALGEOCODINGURI = _(u'PoliticalGeocodingURI')
LABEL_DCATDE_ORIGINATOR = _(u'Originator')
LABEL_DCT_CONFORMSTO = _(u'Standards')
LABEL_DCT_CONTRIBUTOR = _(u'Contributor')
LABEL_DCT_CREATOR = _(u'Creator')
LABEL_DCT_DESCRIPTION = _(u'Description')
LABEL_DCT_FORMAT = _(u'Format')
LABEL_DCT_HASPART = _(u'Parts')
LABEL_DCT_IDENTIFIER = _(u'Identifier')
LABEL_DCT_ISPARTOF = _(u'Parent Catalog')
LABEL_DCT_ISSUED = _(u'Issued')
LABEL_DCT_LANGUAGE = _(u'Languages')
LABEL_DCT_LICENSE = _(u'License')
LABEL_DCT_MODIFIED = _(u'Modified')
LABEL_DCT_PUBLISHER = _(u'Publisher')
LABEL_DCT_RIGHTS = _(u'Rights')
LABEL_DCT_SPATIAL = _(u'Spatial relevance')
LABEL_DCT_THEMETAXONOMY = _(u'Theme Taxonomy')
LABEL_DCT_TITLE = _(u'Title')
LABEL_FOAF_HOMEPAGE = _(u'Homepage')
LABEL_FOAF_LANDINGPAGE = _(u'Landing page')
LABEL_FOAF_PAGE = _(u'Page')
LABEL_FOLDER_AGENTS = _(u'Folder containing agents')
LABEL_FOLDER_FORMATS = _(u'Folder containing formats')
LABEL_FOLDER_LICENSES = _(u'Folder containing licenses')
LABEL_FOLDER_LOCATIONS = _(u'Folder containing locations')
LABEL_FOLDER_PUBLISHERS = _(u'Folder containing publishers')
LABEL_FOLDER_STANDARDS = _(u'Folder containing standards')
LABEL_OWL_VERSIONINFO = _(u'Version info')
LABEL_RDF_ABOUT = _(u'Access URI')
LABEL_RDFS_ISDEFINEDBY = _(u'Definition URI')
LABEL_SETTINGS_BASE = _(u'PKAN Base Settings')
LABEL_SETTINGS_FOLDERS = _(u'PKAN Folder Settings')
LABEL_SETTINGS_IMPORTS = _(u'PKAN Import Settings')
LABEL_SETTINGS_IMPORTS_DCT_LICENSEDOCUMENT = _('DCT:LicenseDocument Sources')
LABEL_SETTINGS_IMPORTS_SKOS_CONCEPT = _('SKOS:Concept Sources')
LABEL_SKOS_INSCHEME = _(u'Concept scheme URI')
LABEL_URL = _(u'URL')

STATUS_REGISTRY_UPDATED = _(
    u'Registry has been updated. Please reload this page.',
)
