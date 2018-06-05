# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde import _
from pkan.dcatapde.utils import get_available_languages_iso
from pkan.dcatapde.utils import get_available_languages_title
from pkan.dcatapde.utils import get_default_language
from plone.api import content
from plone.api import portal
from plone.i18n.normalizer import idnormalizer
from rdflib import URIRef
from zExceptions import BadRequest
from zope.i18n import translate

import os
import rdflib
import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')


class UpdateObjectsBase(object):

    uri = None
    object_class = surf.ns.SKOS['Concept']
    object_title = 'Class:Object'
    object_dx_class = 'Dexterityclass'
    target_folder = None
    mapping = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.default_language = get_default_language()
        self.available_languages = get_available_languages_iso()
        self.available_languages_title = get_available_languages_title()

        if self.uri.startswith('http') or self.uri.startswith('/'):
            pass
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.uri = os.path.join(dir_path, self.uri)

    def load_objects_from_rdf(self):

        store = surf.Store(
            reader='rdflib',
            writer='rdflib',
            rdflib_store='IOMemory',
        )
        # Get a new surf session
        session = surf.Session(store)
        # Load the license list
        store.load_triples(source=self.uri)
        # Define the License class as an skos:concept object
        Object = session.get_class(self.object_class)
        # Get the licenses objects
        objects = Object.all().full()

        return objects

    def import_object(self, obj):
        params = {}
        for key, value in self.mapping.items():
            attribute = getattr(obj, value)
            # deal wth more than one attribute, e.g. different languages
            #  in Literals
            if isinstance(attribute, URIRef):
                att_data = unicode(attribute)
            elif isinstance(attribute.first, rdflib.term.Literal):
                att_data = {}
                for literal in attribute:
                    # check if language attribute exists
                    try:
                        lang = literal.language
                    except AttributeError:
                        lang = self.default_language
                    if lang is None:
                        lang = self.default_language
                    lang = unicode(lang)

                    if lang in self.available_languages:
                        lang = self.available_languages[lang]
                    if lang not in self.available_languages_title:
                        continue
                    att_data[lang] = unicode(literal)

            else:
                if not attribute.first:
                    att_data = None
                else:
                    att_data = unicode(attribute.first.lower())

            params[key] = att_data
        return params

    def import_objects(self, objects):

        good_count = 0
        ignored_count = 0
        for obj in objects:
            params = self.import_object(obj)

            # Special case of adms_identifier. Target type is string not
            # i18ntext. Therefore no dict but string has to be extracted
            attribute = getattr(obj, 'dc_identifier')
            att_data = unicode(attribute.first)
            params['dc_identifier'] = att_data

            # Special case of isDefiendBy. If not given use rdfabout URI
            attribute = getattr(obj, 'rdfs_isDefinedBy')
            if attribute:
                att_data = unicode(attribute.first)
            else:
                att_data = unicode(getattr(obj, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # if there is no title use the identifier
            if not params['dct_title']:
                params['dct_title'] = params['dc_identifier']

            if isinstance(params['dc_identifier'], dict):
                id = params['dc_identifier'][self.default_language]
            elif isinstance(params['dc_identifier'], list):
                id = params['dc_identifier'][0]
            else:
                id = params['dc_identifier']
            id = idnormalizer.normalize(id)

            if isinstance(params['dct_title'], dict):
                title = params['dct_title'][self.default_language]
            elif isinstance(params['dct_title'], list):
                title = params['dct_title'][0]
            else:
                title = params['dct_title']

            try:
                # create a license document object
                content.create(
                    container=self.context,
                    type=self.object_dx_class,
                    id=id,
                    title=title,
                    **params)
            # skip already existing licenses
            except BadRequest:
                ignored_count += 1
                continue
            else:
                good_count += 1
        return good_count, ignored_count

    def __call__(self):
        # get the surf license objects
        objects = self.load_objects_from_rdf()
        # Import the licenses into dexterity objects
        good_count, ignored_count = self.import_objects(objects)

        # Todo : Logging or response to user
        msg = _("""Imported ${good_count} ${object_title} items.
        Ignored ${ignored_count} ${object_title} items.""", mapping={
            'object_title': self.object_title,
            'good_count': good_count,
            'ignored_count': ignored_count,
        })
        msg = translate(msg, context=self.request)
        portal.show_message(message=msg, request=self.request)
        url = '/'.join([
            portal.get().absolute_url(),
            self.target_folder,
        ])
        self.request.response.redirect(url)
        return u''
