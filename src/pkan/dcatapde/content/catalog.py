# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.catalog import add_catalog
from pkan.dcatapde.constants import CT_Catalog
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
    """ Marker interfce and Dexterity Python Schema for Catalog
    """


    dct_title = I18NTextLine(
        title=_(u'Title'),
        required=True,
    )

    dct_description = I18NText(
        title=_(u'Description'),
        required=True,
    )

    form.widget(
        'dct_publisher',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Publisher'),
        initial_path='/publisher/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        }
    )

    dct_publisher = RelationChoice(
        title=_(u'Publisher'),
        description=_(u'Add a new publisher or chose one from the list of publishers'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    form.widget(
        'dct_license',
        RelatedItemsFieldWidget,
        content_type='dct_licensedocument',
        content_type_title=_(u'License'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': ['dct_licensedocument'],
        }
    )

    dct_license = RelationChoice(
        title=_(u'License'),
        description=_(u'Add a new license or chose one from the list of licenses'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    foaf_homepage = schema.URI(
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
        if not self.context.dct_title:
            return ""
        if isinstance(self.context.dct_title, unicode):
            return self.context.dct_title
        """Get title from i18nfield"""
        default_language =portal.get_default_language()[:2]
        if default_language in self.context.dct_title:
            return self.context.dct_title[default_language]
        else:
            current_language = portal.get_current_language()[:2]
            if current_language in self.context.dct_title:
                return self.context.dct_title[current_language]

        return self.context.dct_title[self.context.dct_title.keys()[0]]


class CatalogDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Catalog

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_catalog(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
