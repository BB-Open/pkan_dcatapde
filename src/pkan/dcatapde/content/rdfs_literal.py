# -*- coding: utf-8 -*-
"""RDFliteral Content Type."""

from datetime import date
from datetime import datetime
from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT
from plone.dexterity.content import Item
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from SPARQLWrapper.SmartWrapper import Value
from zope.interface import implementer

import dateutil


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
    _ns_class = 'Literal'

    dct_title = I18NTextProperty(IRDFSLiteral['dct_title'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()


def value2plone(literal, field=None):
    if not field:
        return literal.value
    else:
        val = literal.value
        # If we have a field supplied we can make assumptions
        if field['type'] == date:
            if isinstance(val, str):
                val = dateutil.parser.parse(val)
            if isinstance(val, date):
                return val
            if isinstance(val, datetime):
                return val.date
        elif field['type'] == datetime:
            if isinstance(val, str):
                val = dateutil.parser.parse(val)
            return val
        return val


def literal2plone(literal, field=None):
    if isinstance(literal, Value):
        return value2plone(literal, field)
    val = literal.toPython()
    # if no field specified we can only convert to
    # python and hope
    if not field:
        return val
    # If we have a field supplied we can make assumptions
    if field['type'] == date:
        if isinstance(val, str):
            val = dateutil.parser.parse(val)
        if isinstance(val, date):
            return val
        if isinstance(val, datetime):
            return val.date
    elif field['type'] == datetime:
        if isinstance(val, str):
            val = dateutil.parser.parse(val)
        return val
    else:
        val = literal.toPython()

    return val
