# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope.interface import implementer

import zope.schema as schema


class ICatalog(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Catalog
    """


    title18n = I18NTextLine(
        title=_(u'Title'),
        required=True,
    )

    description18n = I18NText(
        title=_(u'Description'),
        required=True,
    )

    form.widget(
        'publisher',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Publisher'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        }
    )

    publisher = RelationChoice(
        title=_(u'Publisher'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    license = schema.URI(
        title=_(u'License'),
        required=True
    )

    homepage = schema.URI(
        title=(u'Homepage'),
        required=False
    )

    dct_issued = schema.Date(
        title=(u'Issued'),
        required=False
    )

    dct_modified = schema.Date(
        title=(u'Modified'),
        required=False
    )


@implementer(ICatalog)
class Catalog(Container):
    """
    """
    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromCatalog(self).title
        return self._Title

from plone.app.content.interfaces import INameFromTitle
from plone.api import portal

class INameFromCatalog(INameFromTitle):

    def title(self):
        """Return a processed title"""


@implementer(INameFromCatalog)
class NameFromCatalog(object):

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        if isinstance(self.context.title18n, unicode):
            return self.context.title18n
        """Get title from i18nfield"""
        default_language =portal.get_default_language()[:2]
        if default_language in self.context.title18n:
            return self.context.title18n[default_language]
        else:
            current_language = portal.get_current_language()[:2]
            if current_language in self.context.title18n:
                return self.context.title18n[current_language]

        return self.context.title18n[self.context.title18n.keys()[0]]

class CatalogDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Catalog

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_catalog(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
