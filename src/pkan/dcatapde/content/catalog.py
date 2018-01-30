# -*- coding: utf-8 -*-
"""Catalog Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_Catalog
from pkan.dcatapde.constants import CT_DCT_LICENSE_DOCUMENT
from plone.api import portal
from plone.app.content.interfaces import INameFromTitle
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope.interface import implementer

import zope.schema as schema


class ICatalog(model.Schema):
    """Marker interfce and Dexterity Python Schema for Catalog."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=True,
        title=_(u'Description'),
    )

    form.widget(
        'dct_publisher',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Publisher'),
        initial_path='/publisher/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dct_publisher = RelationChoice(
        description=_(
            u'Add a new publisher or chose one from the list of publishers',
        ),
        required=True,
        title=_(u'Publisher'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_license',
        RelatedItemsFieldWidget,
        content_type=CT_DCT_LICENSE_DOCUMENT,
        content_type_title=_(u'License'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [CT_DCT_LICENSE_DOCUMENT],
        },
    )

    dct_license = RelationChoice(
        description=_(
            u'Add a new license or chose one from the list of licenses',
        ),
        required=True,
        title=_(u'License'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    foaf_homepage = schema.URI(
        required=False,
        title=(u'Homepage'),
    )

    dct_issued = schema.Date(
        required=False,
        title=(u'Issued'),
    )

    dct_modified = schema.Date(
        required=False,
        title=(u'Modified'),
    )


@implementer(ICatalog)
class Catalog(Container):
    """Catalog Content Type."""

    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromCatalog(self).title
        return self._Title


class INameFromCatalog(INameFromTitle):
    """Get name from catalog title."""

    def title(self):
        """Return a processed title."""


@implementer(INameFromCatalog)
class NameFromCatalog(object):
    """Get name from catalog title."""

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        if not self.context.dct_title:
            return ''
        if isinstance(self.context.dct_title, unicode):
            return self.context.dct_title
        # Get title from i18nfield
        default_language = portal.get_default_language()[:2]
        if default_language in self.context.dct_title:
            return self.context.dct_title[default_language]
        else:
            current_language = portal.get_current_language()[:2]
            if current_language in self.context.dct_title:
                return self.context.dct_title[current_language]

        return self.context.dct_title[self.context.dct_title.keys()[0]]


class CatalogDefaultFactory(DexterityFactory):
    """Custom DX factory for Catalog."""

    def __init__(self):
        self.portal_type = CT_Catalog

    def __call__(self, *args, **kw):
        from pkan.dcatapde.api.catalog import clean_catalog

        data, errors = clean_catalog(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
