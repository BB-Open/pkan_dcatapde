# -*- coding: utf-8 -*-
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form import validator, util

from z3c.form.browser.radio import RadioFieldWidget
from zope.component import provideAdapter, adapter
from zope.interface import implementer, alsoProvides
import zope.schema as schema

from pkan.dcatapde import _

from foafagent import IFoafagent

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

    add_title = schema.List(
         title=_(u'Translated Title'),
         required=False,
         value_type = schema.Object(ILiteral),
    )

    add_description = schema.List(
         title=_(u'Translated Description'),
         required=False,
         value_type = schema.Object(ILiteral)
    )

    publisher = schema.Object(
        title=_(u'Publisher'),
        required=True,
        schema=IFoafagent
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

alsoProvides(ILiteral, IFoafagent)
#InqbusWidgetValidatorDiscriminators( DCT_TitelValidator, field=ICatalog['dct_title'])


@implementer(ICatalog)
class Catalog(Container):
    """
    """

from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(ICatalog, Catalog)
