# -*- coding: utf-8 -*-
import zope.schema as schema
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.namedfile.interfaces import INamedImageField
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NTextLine, I18NText
from z3c.form import validator, util
from z3c.relationfield import RelationChoice
from zope.component import provideAdapter, adapter
from zope.interface import implementer, alsoProvides

from foafagent import IFoafagent
from pkan.dcatapde import _
from pkan.dcatapde.content.literal import ILiteral


def InqbusWidgetValidatorDiscriminators(validator, context=None, request=None, view=None, field=None, widget=None):

    # Find a unique classname for the new validation adapter utilizing classname of the validator, name of the schema,
    # name of the field
#    validator_classname = "_".join([validator.__class__.__name__, field.interface.__name__, field.__name__ ])
    # make a copy of the validators factory class
#    validator_adapter = type(validator_classname , validator.__bases__, dict(validator.__dict__))
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
        # if the context is no ICustomer we are in an add form
#        if res:
#            raise Invalid(translate(_(u"The customer number given is already in use!"),
#                          target_language=get_current_language()))



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

    publisher = RelationChoice(
        title=_(u'Publisher'),
        vocabulary="plone.app.vocabularies.Catalog",
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
#InqbusWidgetValidatorDiscriminators( DCT_TitelValidator, field=ICatalog['dct_title'])


@implementer(ICatalog)
class Catalog(Container):
    """
    """

from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(ICatalog, Catalog)

from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter, getIfName
from zope.component.interfaces import IFactory
from zope.component import queryUtility

@implementer(IObjectFactory)
class ImageFactory(FactoryAdapter):
    """
    """

    def __call__(self, value):
        factory = queryUtility(IFactory, name='catalog')
        return factory()

name = getIfName(INamedImageField)
#zope.component.provideAdapter(ImageFactory, name=name)
