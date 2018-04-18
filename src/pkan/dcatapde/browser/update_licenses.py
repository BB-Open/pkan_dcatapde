# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import FOLDER_LICENSES
from pkan.dcatapde.constants import VOCAB_SOURCES
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_TITLE
from plone.api import content
from plone.api import portal
from zope.i18n import translate

import rdflib
import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')


class UpdateLicenses(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def load_licenses_from_rdf(self):
        uri = VOCAB_SOURCES[CT_DCT_LICENSEDOCUMENT]

        store = surf.Store(
            reader='rdflib',
            writer='rdflib',
            rdflib_store='IOMemory',
        )
        # Get a new surf session
        session = surf.Session(store)
        # Load the license list
        store.load_triples(source=uri)
        # Define the License class as an owl:class object
        License = session.get_class(surf.ns.OWL['Class'])
        # Get the licenses objects
        licenses = License.all().full()

        return licenses

    def __call__(self):
        # get the surf license objects
        licenses = self.load_licenses_from_rdf()

        default_language = portal.get_default_language()

        count = 0
        for license in licenses:
            # map the properties
            mapping = {
                'dct_title': 'rdfs_label',
                'dct_description': 'rdfs_comment',
                'rdfs_subClassOf': 'rdfs_subClassOf',
            }
            params = {}
            for key, value in mapping.items():
                attribute = getattr(license, value)
                # deal wth more than one attribute, e.g. different languages
                #  in Literals
                if isinstance(attribute.first, rdflib.term.Literal):
                    att_data = {}
                    for literal in attribute:
                        # check if language attribute exists
                        try:
                            lang = literal.language
                        except AttributeError:
                            lang = default_language
                        lang = unicode(lang)
                        if lang in AVAILABLE_LANGUAGES_ISO:
                            lang = AVAILABLE_LANGUAGES_ISO[lang]
                        if lang not in AVAILABLE_LANGUAGES_TITLE:
                            continue
                        att_data[lang] = unicode(literal)

                else:
                    att_data = unicode(attribute.first)

                params[key] = att_data

            # Special case of adms_identifier. Target type is string not
            # i18ntext. Therefore no dict but string has to be extracted
            attribute = getattr(license, 'adms_identifier')
            att_data = unicode(attribute.first)
            params['adms_identifier'] = att_data

            # Special case of isDefiendBy. If not given use rdfabout URI
            attribute = getattr(license, 'rdfs_isDefinedBy')
            if attribute:
                att_data = unicode(attribute.first)
            else:
                att_data = unicode(getattr(license, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # create a license document object
            try:
                content.create(
                    container=self.context,
                    type=CT_DCT_LICENSEDOCUMENT,
                    id=params['adms_identifier'],
                    **params)
            except Exception:
                continue
            else:
                count += 1

            # Todo : Logging or response to user

        msg = _('Imported ${count} DCT:LicenseDocument items.', mapping={
            'count': count,
        })
        msg = translate(msg, context=self.request)
        portal.show_message(message=msg, request=self.request)
        url = '/'.join([
            portal.get().absolute_url(),
            FOLDER_LICENSES,
        ])
        self.request.response.redirect(url)
        return u''
