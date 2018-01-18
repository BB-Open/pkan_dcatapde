# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter
from z3c.form.object import getIfName
from zope.component import queryUtility
from zope.component.interfaces import IFactory
from zope.interface import implementer

import zope.component
import zope.schema as schema


class IFoafagent(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Foafagent
    """

    # URI of FOAF agent has to be required. Since agents can be referenced from
    # several locations at once without a single fixed URI different access paths could arise
    rdf_about = schema.URI(
         title=_(u'Access URI'),
         required=True
    )


@implementer(IFoafagent)
class Foafagent(Item):
    """
    """
    portal_type = 'foafagent'
    namespace_class = 'foaf:agent'




