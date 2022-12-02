# -*- coding: utf-8 -*-

from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements

from pkan.dcatapde import utils
from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.content.dcat_dataset import IDCATDataset


class CatalogEditForm(edit.DefaultEditForm):

    schema = IDCATCatalog

    def __init__(self, context, request, ti=None):
        super(CatalogEditForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)


CatalogEditView = layout.wrap_form(CatalogEditForm)
classImplements(CatalogEditView, IDexterityEditForm)


class DatasetEditForm(edit.DefaultEditForm):

    schema = IDCATDataset

    def __init__(self, context, request, ti=None):
        super(DatasetEditForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)


DatasetEditView = layout.wrap_form(DatasetEditForm)
classImplements(DatasetEditView, IDexterityEditForm)
