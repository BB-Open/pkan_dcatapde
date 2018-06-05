# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""

from pkan.dcatapde.browser.update_views.update_base import UpdateObjectsBase
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import FOLDER_LICENSES
from pkan.dcatapde.constants import VOCAB_SOURCES


# map the properties
MAPPING = {
    'dct_title': 'dc_identifier',
    'dct_description': 'skos_prefLabel',
    'skos_inScheme': 'skos_inScheme',
}


class UpdateLicenses(UpdateObjectsBase):

    uri = VOCAB_SOURCES[CT_DCT_LICENSEDOCUMENT]
    object_title = 'DCT:LicenseDocument'
    object_dx_class = CT_DCT_LICENSEDOCUMENT
    target_folder = FOLDER_LICENSES
    mapping = MAPPING
