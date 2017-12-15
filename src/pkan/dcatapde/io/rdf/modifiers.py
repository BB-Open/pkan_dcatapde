""" Modifiers """
import re
import sys
import rdflib
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import log
from zope.component import adapts
from zope.interface import implements, providedBy
from plone.dexterity.interfaces import IDexterityContent

try:
    from plone.app.multilingual.interfaces import ITranslationManager
    has_plone_multilingual = False
except ImportError:
    has_plone_multilingual = False

from .interfaces import ISurfResourceModifier

ILLEGAL_XML_CHARS_PATTERN = re.compile(
    u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]'
)


class WorkflowStateModifier(object):
    """Adds workflow information information to rdf resources
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        plone_portal_state = self.context.restrictedTraverse(
            '@@plone_portal_state')
        portal_url = plone_portal_state.portal_url()

        workflowTool = getToolByName(self.context, "portal_workflow")
        wfs = workflowTool.getWorkflowsFor(self.context)
        wf = None
        for wf in wfs:
            if wf.isInfoSupported(self.context, "portal_workflow"):
                break

        status = workflowTool.getInfoFor(self.context, "review_state", None)
        if status is not None:
            status = ''.join([portal_url,
                              "/portal_workflow/",
                              getattr(wf, 'getId', lambda: '')(),
                              "/states/",
                              status])
            try:
                setattr(resource, '%s_%s' % ("eea", "hasWorkflowState"),
                        rdflib.URIRef(status))
            except Exception:
                log.log('RDF marshaller error for context[workflow_state]'
                        '"%s": \n%s: %s' %
                        (self.context.absolute_url(),
                         sys.exc_info()[0], sys.exc_info()[1]),
                        severity=log.logging.WARN)
        return resource


# Archetypes modifiers ported to dexterity
class IsPartOfModifier(object):
    """Adds dcterms_isPartOf information to rdf resources
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        parent = self.context.getParentNode()
        wftool = getToolByName(self.context, 'portal_workflow')
        if parent is not None:
            try:
                state = wftool.getInfoFor(parent, 'review_state')
            except WorkflowException:
                state = 'published'

            if state == 'published':
                parent_url = parent.absolute_url()
                resource.dcterms_isPartOf = \
                    rdflib.URIRef(parent_url)


class TranslationInfoModifier(object):
    """Adds translation info
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        context = self.context

        # ZZZ: should watch for availability of plone.app.multilingual
        if has_plone_multilingual:
            translations = ITranslationManager(
                context).get_translated_languages()

            if translations:
                translations_objs = [ITranslationManager.get_translation(o)
                                     for o in translations]
                resource.eea_hasTranslation = \
                    [rdflib.URIRef(o.absolute_url()) for o in translations_objs
                     if o.absolute_url() != context.absolute_url()]
            else:
                resource.eea_isTranslationOf = \
                    rdflib.URIRef(context.absolute_url())
        else:
            resource.eea_hasTranslation = ['No Translation']
            return


class ProvidedInterfacesModifier(object):
    """Adds information about provided interfaces
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        provides = ["%s.%s" % (iface.__module__ or '', iface.__name__)
                    for iface in providedBy(self.context)]
        resource.eea_objectProvides = provides


class SearchableTextInModifier(object):
    """Adds searchable text info
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        resource.dcterms_abstract = ILLEGAL_XML_CHARS_PATTERN.sub(
            '', self.context.SearchableText())


class RelatedItemsModifier(object):
    """Adds dcterms:references
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        if not getattr(self.context, 'relatedItems', None):
            return

        resource.dcterms_references = [
            rdflib.URIRef(o.to_object.absolute_url())
            for o in self.context.relatedItems]


# This one comes from eea.dataservices
class BaseFileModifier(object):
    """Adds dcterms:format
    """

    field = ''

    implements(ISurfResourceModifier)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """change the rdf resource
        """
        item = getattr(self.context, self.field)
        if not item:
            return

        setattr(resource, "dcterms_format", [item.contentType])
