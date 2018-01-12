# -*- coding: utf-8 -*-
from foafagent import IFoafagent
from pkan.dcatapde import _
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.namedfile import field as namedfile
from plone.namedfile.interfaces import INamedImageField
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.form import util
from z3c.form import validator
from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter
from z3c.form.object import getIfName
from z3c.form.object import registerFactoryAdapter
from z3c.relationfield import RelationChoice
from zope.component import adapter
from zope.component import provideAdapter
from zope.component import queryUtility
from zope.component.interfaces import IFactory
from zope.interface import alsoProvides
from zope.interface import implementer

import zope.schema as schema


def InqbusWidgetValidatorDiscriminators(validator, context=None,
                                        request=None, view=None, field=None,
                                        widget=None):

    # Make the copy to a well shaped adapter
    validator_adapter = adapter(
        util.getSpecification(context),
        util.getSpecification(request),
        util.getSpecification(view),
        util.getSpecification(field),
        util.getSpecification(widget))(validator)

    # register the new validation adapter
    provideAdapter(validator_adapter)


class DCT_TitelValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        return True


class ICatalog(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Catalog
    """

    # add_title = schema.List(
    #      title=_(u'Translated Title'),
    #      required=False,
    #      value_type = schema.Object(ILiteral),
    # )

    add_title = I18NTextLine(
        title=_(u'Translated Title'),
        required=False,
    )

    # add_description = schema.List(
    #      title=_(u'Translated Description'),
    #      required=False,
    #      value_type = schema.Object(ILiteral)
    # )

    add_description = I18NText(
        title=_(u'Translated Description'),
        required=False,
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

    image = namedfile.NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )


alsoProvides(ILiteral, IFoafagent)


@implementer(ICatalog)
class Catalog(Container):
    """
    """


registerFactoryAdapter(ICatalog, Catalog)


@implementer(IObjectFactory)
class ImageFactory(FactoryAdapter):
    """
    """

    def __call__(self, value):
        factory = queryUtility(IFactory, name='catalog')
        return factory()


name = getIfName(INamedImageField)
