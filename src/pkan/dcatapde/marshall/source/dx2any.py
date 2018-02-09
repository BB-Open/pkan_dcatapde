# -*- coding: utf-8 -*-
"""Recursive crawler through objects and properties for marshalling"""

from pkan.dcatapde.marshall.interfaces import IMarshallSource
# from pkan.dcatapde.marshall.source.interfaces import IDXField2Any
from plone.api.portal import get_tool
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
# from plone.dexterity.interfaces import IDexterityContent
# from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel.interfaces import FIELDSETS_KEY
from zope.component import adapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import getFieldsInOrder


def non_fieldset_fields(schema):
    """Return fields not in fieldset."""
    fieldset_fields = []
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

    for fieldset in fieldsets:
        fieldset_fields.extend(fieldset.fields)

    fields = [info[0] for info in getFieldsInOrder(schema)]

    return [f for f in fields if f not in fieldset_fields]


def get_ordered_fields(fti):
    """Return fields in fieldset order.

    NOTE: code extracted from collective.excelexport. Original comments
    preserved

    this code is much complicated because we have to get sure
    we get the fields in the order of the fieldsets
    the order of the fields in the fieldsets can differ
    of the getFieldsInOrder(schema) order...
    that's because fields from different schemas
    can take place in the same fieldset
    """
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


@implementer(IMarshallSource)
@adapter(Interface, Interface)
class DX2Any(object):
    """Default marshaller for dexterity."""

    _whitelist = []
    _blacklist = []

    namespace = 'rdf'
    ns_class = 'Literal'

    def __init__(self, context, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target

    @property
    def properties(self):
        """Return properties.

        :return:
        """
        ptypes = get_tool('portal_types')
        fti = ptypes[self.context.portal_type]

        result = {}
        for field_name, field in get_ordered_fields(fti):
            if field_name in self._blacklist:
                continue
            if self._whitelist and not (field_name in self._whitelist):
                continue
            result[field_name] = field

        return result

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        return {}

    def marshall_myself(self):
        """Marshall myself."""
        self.resource = self.marshall_target.marshall(self)

    def marshall_properties(self):
        """Marshall properties."""
        for property_name, property in self.properties.items():
            property_marshaller = queryMultiAdapter(
                (self.context, property, self.marshall_target),
                interface=IMarshallSource,
            )
            if property_marshaller:
                # let the adapter marshall the property
                marshalled_property = property_marshaller.marshall(self)
                self.marshall_target.add_property(
                    self.resource,
                    property_name,
                    marshalled_property,
                )
            else:
                # No adapter can be found, convert the field value to a string.
                value = str(getattr(self.context, property_name))
                self.marshall_target.add_property(
                    self.resource,
                    property_name,
                    value,
                )

    def marshall_contained(self):
        """Marshall contained objects."""
        for item_name, items in self.contained.items():
            for item in items:
                contained_marshaller = queryMultiAdapter(
                    (item, self.marshall_target),
                    interface=IMarshallSource,
                    default=DX2Any(item, self.marshall_target),
                )
                if contained_marshaller:
                    contained_marshaller.marshall()
                    self.marshall_target.set_link(
                        self.resource,
                        item_name,
                        contained_marshaller.resource,
                    )

    def marshall_references(self):
        """Marshall the referenced objects."""
        for item_name, item in self.referenced.items():
            referenced_marshaller = queryMultiAdapter(
                (item, self.marshall_target),
                interface=IMarshallSource,
                default=DX2Any(item, self.marshall_target),
            )
            if referenced_marshaller:
                referenced_marshaller.marshall()

                self.marshall_target.set_link(
                    self.resource,
                    item_name,
                    referenced_marshaller.resource,
                )

    def marshall(self):
        """Marshall properties, contained items and related items."""
        self.marshall_myself()
        self.marshall_properties()
        self.marshall_references()
        self.marshall_contained()
        self.resource.update()
        self.resource.save()


@implementer(IMarshallSource)
@adapter(Interface, Interface)
class DXField2Any(object):
    """Default marshaller for dexterity."""

    def __init__(self, context, field, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.field = field
        self.marshall_target = marshall_target

    def marshall_myself(self):
        """Marshall myself."""
        self.resource = self.marshall_target.marshall(self)

    def marshall(self):
        self.marshall_myself()
        # a = IDexterityContent
