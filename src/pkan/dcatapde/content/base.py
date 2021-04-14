# -*- coding: utf-8 -*-
"""Base Content Types."""
from pkan.dcatapde import i18n
from pkan.dcatapde.structure.interfaces import IStructure
from pkan.dcatapde.utils import get_current_language
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.supermodel import model

import zope.schema as schema


class IDCAT(model.Schema):
    """Marker interface for all DCAT-AP.de Content Types"""

    read_permission(dct_identifier='pkan.dcatapde.ProviderDataEditor')
    write_permission(dct_identifier='pkan.dcatapde.ProviderDataEditor')
    dct_identifier = schema.URI(
        required=False,
        title=i18n.LABEL_DCT_IDENTIFIER,
        description=i18n.IDENTIFIER_DESCRIPTION,
    )

    read_permission(adms_identifier='pkan.dcatapde.ProviderDataEditor')
    write_permission(adms_identifier='pkan.dcatapde.ProviderDataEditor')
    adms_identifier = schema.URI(
        required=False,
        title=i18n.LABEL_ADMS_IDENTIFIER,
        description=i18n.IDENTIFIER_DESCRIPTION,
    )

#    read_permission(uri_in_triplestore='pkan.dcatapde.Admin')
#    write_permission(uri_in_triplestore='pkan.dcatapde.Admin')
#    uri_in_triplestore = schema.URI(
#        required=False,
#        title=_(u'Uri in Triplestore'),
#    )

    model.fieldset(
        'object_identifier',
        label=i18n.FIELDSET_INTERNAL_INFO,
        fields=[
            'dct_identifier',
            'adms_identifier',
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
                all_titles = getattr(all_titles, 'data', all_titles)
                if not all_titles:
                    continue
                if isinstance(all_titles, dict):
                    curr_lang = get_current_language()
                    if curr_lang and \
                            curr_lang in all_titles and \
                            all_titles[curr_lang]:
                        return all_titles[curr_lang]
                    title = str(list(all_titles.items())[0][1])
                elif isinstance(all_titles, list):
                    title = str(all_titles[0])
                else:
                    title = str(all_titles)
            except (KeyError, AttributeError):
                continue
            if title:
                break
        if title:
            return title
        else:
            return ''

    def desc_from_desc_field(self):
        desc = None
        struct = IStructure(self)
        for desc_field in struct.desc_field:
            try:
                all_descs = getattr(self, desc_field)
                if not all_descs:
                    continue
                if isinstance(all_descs, dict):
                    desc = str(list(all_descs.items())[0][1])
                elif isinstance(all_descs, list):
                    desc = str(all_descs[0])
                else:
                    desc = str(all_descs)
            except KeyError:
                continue
            if desc:
                break
        if desc:
            return desc
        else:
            return ''


def add_obj_identifier(obj, event):

    if not obj.dct_identifier:
        obj.dct_identifier = obj.absolute_url()

    if not obj.adms_identifier:
        obj.adms_identifier = obj.absolute_url()
