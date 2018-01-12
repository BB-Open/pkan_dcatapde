# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.catalog import add_catalog
from pkan.dcatapde.constants import CT_Catalog
from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde.content.foafagent import IFoafagent
from plone.api.portal import get_current_language
from plone.autoform.directives import omitted
from plone.dexterity.browser import add
from z3c.form import button
from z3c.form.interfaces import ActionExecutionError
from z3c.form.object import registerFactoryAdapter
from z3c.pt.pagetemplate import ViewPageTemplateFile
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema.fieldproperty import FieldProperty

import zope.schema as schema


class IPublisher(IFoafagent):

    name = schema.TextLine(
        title=_(u'Name'),
        required=False
    )

    available = schema.Choice(
        title=_(u'Available Publisher'),
        # TODO: Implement Vocabulary
        vocabulary='pkan.dcatapde.FoafagentVocabulary',
        required=False,
    )


@implementer(IPublisher)
class Publisher(object):
    name = FieldProperty(IPublisher['name'])
    available = FieldProperty(IPublisher['available'])


registerFactoryAdapter(IPublisher, Publisher)


class CatalogAddSchema(ICatalog):
    omitted('publisher')

    # is an unstored python object, you can ask it for
    # attributes to create or set publisher
    new_publisher = schema.Object(
        title=_(u'Publisher'),
        schema=IPublisher
    )


class CatalogAddForm(add.DefaultAddForm):
    portal_type = CT_Catalog
    schema = CatalogAddSchema

    def updateWidgets(self, prefix=None):
        super(CatalogAddForm, self).updateWidgets()

        self.widgets['new_publisher'].template = \
            ViewPageTemplateFile('templates/oneline.pt')
        self.widgets['new_publisher'].addClass('oneline-widget')

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return

        try:
            catalog = add_catalog(self.context, **data)
        except AssertionError as e:
            msg = translate(e.message, target_language=get_current_language())
            raise ActionExecutionError(Invalid(msg))

        self.request.response.redirect(catalog.absolute_url())


class CatalogAddView(add.DefaultAddView):
    form = CatalogAddForm
