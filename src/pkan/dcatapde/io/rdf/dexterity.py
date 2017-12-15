""" rdfmarshaller adapters for dexterity content
"""

import sys

from zope.component import (adapts, getMultiAdapter, getUtility, queryAdapter,
                            queryMultiAdapter)
from zope.schema import getFieldsInOrder

import surf
from .interfaces import IDXField2Surf
from .interfaces import (IFieldDefinition2Surf, ISurfSession,
                                          IValue2Surf)
from .export import GenericObject2Surf
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityContent, IDexterityFTI
from plone.supermodel.interfaces import FIELDSETS_KEY
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import log


def non_fieldset_fields(schema):
    """ return fields not in fieldset """
    fieldset_fields = []
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

    for fieldset in fieldsets:
        fieldset_fields.extend(fieldset.fields)

    fields = [info[0] for info in getFieldsInOrder(schema)]

    return [f for f in fields if f not in fieldset_fields]


def get_ordered_fields(fti):
    """ return fields in fieldset order """
    # NOTE: code extracted from collective.excelexport. Original comments
    # preserved

    # this code is much complicated because we have to get sure
    # we get the fields in the order of the fieldsets
    # the order of the fields in the fieldsets can differ
    # of the getFieldsInOrder(schema) order...
    # that's because fields from different schemas
    # can take place in the same fieldset
    schema = fti.lookupSchema()
    fieldset_fields = {}
    ordered_fieldsets = ['default']

    for fieldset in schema.queryTaggedValue(FIELDSETS_KEY, []):
        ordered_fieldsets.append(fieldset.__name__)
        fieldset_fields[fieldset.__name__] = fieldset.fields

    if fieldset_fields.get('default', []):
        fieldset_fields['default'] += non_fieldset_fields(schema)
    else:
        fieldset_fields['default'] = non_fieldset_fields(schema)

    # Get the behavior fields
    fields = getFieldsInOrder(schema)

    for behavior_id in fti.behaviors:
        schema = getUtility(IBehavior, behavior_id).interface

        if not IFormFieldProvider.providedBy(schema):
            continue

        fields.extend(getFieldsInOrder(schema))

        for fieldset in schema.queryTaggedValue(FIELDSETS_KEY, []):
            fieldset_fields.setdefault(
                fieldset.__name__, []).extend(fieldset.fields)
            ordered_fieldsets.append(fieldset.__name__)

        fieldset_fields['default'].extend(non_fieldset_fields(schema))

    ordered_fields = []

    for fieldset in ordered_fieldsets:
        ordered_fields.extend(fieldset_fields[fieldset])

    fields.sort(key=lambda field: ordered_fields.index(field[0]))

    return fields


class Dexterity2Surf(GenericObject2Surf):
    """ Dexterity implementation of the Object2Surf
    """

    adapts(IDexterityContent, ISurfSession)

    dc_map = dict([('title', 'title'),
                   ('description', 'description'),
                   ('creation_date', 'created'),
                   ('modification_date', 'modified'),
                   ('creators', 'creator'),
                   ('subject', 'subject'),
                   # ('effectiveDate', 'issued'),
                   # ('expirationDate', 'expires'),
                   ('rights', 'rights'),
                   # ('contributors', 'contributor'),
                   ('effective', 'issued'),
                   ('expires', 'expires'),
                   ('id', 'productID')])

    _blacklist = ['constrainTypesMode',
                  'locallyAllowedTypes',
                  'immediatelyAddableTypes',
                  'language',
                  'allowDiscussion']
    field_map = {}

    @property
    def blacklist_map(self):
        """ These fields shouldn't be exported """
        ptool = getToolByName(self.context, 'portal_properties')
        props = getattr(ptool, 'rdfmarshaller_properties', None)

        if props:
            return list(
                props.getProperty('%s_blacklist' % self.portalType.lower(),
                                  props.getProperty('blacklist'))
            )

        return self._blacklist

    @property
    def portalType(self):
        """ Portal type """

        return self.context.portal_type.replace(' ', '').replace('.', '')

    @property
    def prefix(self):
        """ Prefix """

        return self.portalType.lower()

    @property
    def subject(self):
        """ Subject """

        return self.context.absolute_url()

    @property
    def namespace(self):
        """ namespace """

        if self._namespace is not None:
            return self._namespace

        ttool = getToolByName(self.context, 'portal_types')
        ftype = ttool[self.context.portal_type]
        surf.ns.register(**{self.prefix: '%s#' % ftype.absolute_url()})
        self._namespace = getattr(surf.ns, self.prefix.upper())

        return self._namespace

    def modify_resource(self, resource, *args, **kwds):
        language = self.context.Language()
        ptypes = getToolByName(self.context, 'portal_types')
        fti = ptypes[self.context.portal_type]

        for fieldName, field in get_ordered_fields(fti):
            if fieldName in self.blacklist_map:
                continue
            fieldAdapter = queryMultiAdapter(
                (field, self.context, self.session),
                interface=IDXField2Surf,
                name=fieldName
            )

            if not fieldAdapter:
                fieldAdapter = getMultiAdapter(
                    (field, self.context, self.session),
                    interface=IDXField2Surf)

            if not fieldAdapter.exportable:
                continue

            try:
                value = fieldAdapter.value()
            except Exception:
                log.log('RDF marshaller error for context[field]'
                        '"%s[%s]": \n%s: %s' %
                        (self.context.absolute_url(), fieldName,
                         sys.exc_info()[0], sys.exc_info()[1]),
                        severity=log.logging.WARN)

                continue

            valueAdapter = queryAdapter(value, interface=IValue2Surf)

            if valueAdapter:
                value = valueAdapter(language=language)

            if not value or value == "None":
                continue

            prefix = (fieldAdapter.prefix or self.prefix).replace('.', '')

            fieldName = fieldAdapter.name

            if fieldName in self.field_map:
                fieldName = self.field_map.get(fieldName)
            elif fieldName in self.dc_map:
                fieldName = self.dc_map.get(fieldName)
                prefix = 'dcterms'

            try:
                setattr(resource, '%s_%s' % (prefix, fieldName), value)
            except Exception:

                log.log(
                    'RDF marshaller error for context[field]'
                    '"%s[%s]": \n%s: %s' % (
                        self.context.absolute_url(), fieldName,
                        sys.exc_info()[0], sys.exc_info()[1]
                    ),
                    severity=log.logging.WARN
                )

        return resource


class DexterityFTI2Surf(GenericObject2Surf):
    """ IObject2Surf implemention for TypeInformations,

    The type informations are persistent objects found in the portal_types """

    adapts(IDexterityFTI, ISurfSession)

    _namespace = surf.ns.RDFS    # we need an open namespage
    _prefix = 'rdfs'

    # fields not to export, i.e Dublin Core
    blacklist_map = ['constrainTypesMode',
                     'locallyAllowedTypes',
                     'immediatelyAddableTypes',
                     'language',
                     'creation_date',
                     'modification_date',
                     'creators',
                     'subject',
                     'effectiveDate',
                     'expirationDate',
                     'contributors',
                     'allowDiscussion',
                     'rights',
                     'nextPreviousEnabled',
                     'excludeFromNav',
                     'creator',
                     'title',
                     'exclude_from_nav',
                     'effective',
                     'expires'
                     ]

    def modify_resource(self, resource, *args, **kwds):
        """ Schema to Surf """

        context = self.context
        session = self.session

        setattr(resource, 'rdfs_label', (context.Title(), u'en'))
        setattr(resource, 'rdfs_comment', (context.Description(), u'en'))
        setattr(resource, 'rdf_id', self.rdfId)
        resource.update()

        # the following hack creates a new instance of a content to
        # allow extracting the full schema, with extended fields
        # Is this the only way to do this?
        # Another way would be to do a catalog search for a portal_type,
        # grab the first object from there and use that as context

        for fieldName, field in get_ordered_fields(context):

            if fieldName in self.blacklist_map:
                continue

            field2surf = queryMultiAdapter(
                (field, context, session), interface=IFieldDefinition2Surf)

            if field2surf is None:
                # NOTE: log a warning

                continue
            field2surf.write()

        return resource
