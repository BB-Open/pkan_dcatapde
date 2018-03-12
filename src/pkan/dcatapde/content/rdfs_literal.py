# -*- coding: utf-8 -*-
"""RDFliteral Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT
from plone.dexterity.content import Item
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer


class IRDFSLiteral(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for RDFLiterla."""

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )


@implementer(IRDFSLiteral)
class RDFLiteral(Item, DCATMixin):
    """SKOSConcept Content Type."""

    portal_type = constants.CT_SKOS_CONCEPT
    content_schema = IRDFSLiteral
    _namespace = 'rdfs'
    _ns_class = 'literal'

    dct_title = I18NTextProperty(IRDFSLiteral['dct_title'])

    def Title(self):
        return unicode(self.dct_title)
