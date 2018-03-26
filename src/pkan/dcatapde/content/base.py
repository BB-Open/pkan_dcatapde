# -*- coding: utf-8 -*-
"""Base Content Types."""
from pkan.dcatapde import _
from pkan.dcatapde import i18n
from pkan.dcatapde.structure.interfaces import IStructure
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model

import zope.schema as schema


class IDCAT(model.Schema):
    """Marker interface for all DCAT-AP.de Content Types"""

    uri_in_triplestore = schema.URI(
        required=False,
        title=_(u'Uri in Triplestore'),
    )

    form.widget(
        'in_harvester',
        AjaxSelectAddFieldWidget,
    )
    in_harvester = schema.Choice(
        description=i18n.HELP_IN_HARVESTER,
        required=False,
        title=i18n.LABEL_IN_HARVESTER,
        vocabulary='pkan.dcatapde.vocabularies.Harvester',
    )

    model.fieldset(
        'internal_info',
        label=i18n.FIELDSET_INTERNAL_INFO,
        fields=[
            'uri_in_triplestore',
            'in_harvester',
        ],
    )


class DCATMixin(object):
    """Catalog Content Type."""

    _index_fields = ['dct_title', 'dct_description']

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return self.Title()

    def title_from_title_field(self):
        title = None
        struct = IStructure(self)
        for title_field in struct.title_field:
            try:
                all_titles = getattr(self, title_field)
                if not all_titles:
                    continue
                if isinstance(all_titles, dict):
                    title = unicode(all_titles.items()[0][1])
                elif isinstance(all_titles, list):
                        title = unicode(all_titles[0])
                else:
                    title = unicode(all_titles)
            except KeyError:
                continue
        return title
