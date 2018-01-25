# -*- coding: utf-8 -*-
"""Modifiers."""

from pkan.dcatapde.io.rdf.interfaces import ISurfResourceModifier
from plone.api.content import get_state
from plone.api.portal import get_tool
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone import log
from zope.component import adapter
from zope.interface import implementer
from zope.interface import providedBy

import rdflib
import re
import sys


try:
    from plone.app.multilingual.interfaces import ITranslationManager
    has_plone_multilingual = False
except ImportError:
    has_plone_multilingual = False


ILLEGAL_XML_CHARS_PATTERN = re.compile(
    u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]',
)


@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class WorkflowStateModifier(object):
    """Add workflow information information to rdf resources."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        plone_portal_state = self.context.restrictedTraverse(
            '@@plone_portal_state')
        portal_url = plone_portal_state.portal_url()

        workflowTool = get_tool('portal_workflow')
        wfs = workflowTool.getWorkflowsFor(self.context)
        wf = None
        for wf in wfs:
            if wf.isInfoSupported(self.context, 'portal_workflow'):
                break

        status = get_state(self.context, 'review_state')
        if status is not None:
            status = ''.join([
                portal_url,
                '/portal_workflow/',
                getattr(wf, 'getId', lambda: '')(),
                '/states/',
                status,
            ])
            try:
                setattr(
                    resource,
                    '{0}_{1}'.format('eea', 'hasWorkflowState'),
                    rdflib.URIRef(status),
                )
            except Exception:
                log.log(
                    'RDF marshaller error for context[workflow_state]'
                    '"{0}": \n{1}: {2}'.format(
                        self.context.absolute_url(),
                        sys.exc_info()[0], sys.exc_info()[1],
                    ),
                    severity=log.logging.WARN,
                )
        return resource


# Archetypes modifiers ported to dexterity
@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class IsPartOfModifier(object):
    """Add dcterms_isPartOf information to rdf resources."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        parent = self.context.getParentNode()
        if parent is not None:
            try:
                state = get_state(parent, 'review_state')
            except WorkflowException:
                state = 'published'

            if state == 'published':
                parent_url = parent.absolute_url()
                resource.dcterms_isPartOf = \
                    rdflib.URIRef(parent_url)


@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class TranslationInfoModifier(object):
    """Add translation info."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        context = self.context

        # ZZZ: should watch for availability of plone.app.multilingual
        if has_plone_multilingual:
            translations = ITranslationManager(
                context,
            ).get_translated_languages()

            if translations:
                translations_objs = [
                    ITranslationManager.get_translation(o)
                    for o in translations
                ]
                resource.eea_hasTranslation = [
                    rdflib.URIRef(o.absolute_url())
                    for o in translations_objs
                    if o.absolute_url() != context.absolute_url()
                ]
            else:
                resource.eea_isTranslationOf = rdflib.URIRef(
                    context.absolute_url(),
                )
        else:
            resource.eea_hasTranslation = ['No Translation']
            return


@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class ProvidedInterfacesModifier(object):
    """Add information about provided interfaces."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        provides = [
            '{0}.{1}'.format(iface.__module__ or '', iface.__name__)
            for iface in providedBy(self.context)
        ]
        resource.eea_objectProvides = provides


@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class SearchableTextInModifier(object):
    """Add searchable text info."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        resource.dcterms_abstract = ILLEGAL_XML_CHARS_PATTERN.sub(
            '',
            self.context.SearchableText(),
        )


@implementer(ISurfResourceModifier)
@adapter(IDexterityContent)
class RelatedItemsModifier(object):
    """Add dcterms:references."""

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        if not getattr(self.context, 'relatedItems', None):
            return

        resource.dcterms_references = [
            rdflib.URIRef(o.to_object.absolute_url())
            for o in self.context.relatedItems
        ]


# This one comes from eea.dataservices

@implementer(ISurfResourceModifier)
class BaseFileModifier(object):
    """Add dcterms:format."""

    field = ''

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource."""
        item = getattr(self.context, self.field)
        if not item:
            return

        setattr(resource, 'dcterms_format', [item.contentType])
