# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from DateTime.DateTime import time
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.content.rdfs_literal import literal2plone
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFXML
from pkan.dcatapde.harvesting.rdf.rdf2plone import RDFProcessor
from pkan.dcatapde.harvesting.rdf.visitors import NT_RESIDUAL
from pkan.dcatapde.structure.sparql import QUERY_P
from pkan.dcatapde.structure.structure import StructRDFSLiteral
from plone.api import content
from plone.api.exc import InvalidParameterError
from rdflib.term import Literal
from rdflib.term import URIRef
from urllib import parse
from zope.component import adapter
from zope.interface import implementer


IFaceToRDFFormatKey = {
    IRDFTTL: RDF_FORMAT_TURTLE,
    IRDFJSONLD: RDF_FORMAT_JSONLD,
    IRDFXML: RDF_FORMAT_XML,
}


def cache_key(func, self):
    """cache key factory for rdf graph. With timeout 300 seconds
    :param func:
    :param self:
    :return:
    """
    key = u'{0}_{1}'.format(
        time() // 300,
        self.harvester.url,
    )
    return key


def handle_identifiers(obj):
    """
    Handle Konv 24/25/26/27
    Deal with duplicates and push trough Id information
    """

    params = {}

    # Special case of dct_identifier. If dct:identifier is set conserve it.
    dct_identifier = str(getattr(obj, 'dct_identifier', None))
    if isinstance(obj, URIRef):
        subject = str(obj)
    else:
        try:
            subject = str(getattr(obj, 'subject'))
        except AttributeError:
            # This is the case for Literal
            subject = None

    # if no dct:Identifier is set
    if dct_identifier is None:
        # set it to the subject
        params['dct_identifier'] = subject
    else:
        # check if dct:Identifier is really an URI
        if parse.urlparse(dct_identifier).scheme != '':
            params['dct_identifier'] = dct_identifier
        else:
            params['dct_identifier'] = subject

            # Special case of adms_identifier. If adms:identifier is set
    # conserve it.
    adms_identifier = str(getattr(obj, 'adms_identifier', None))
    if adms_identifier is not None:
        # check if adms:dientifier is really an URI
        if parse.urlparse(adms_identifier).scheme != '':
            params['adms_identifier'] = adms_identifier
        else:
            params['adms_identifier'] = None
    else:
        params['adms_identifier'] = None

    return params


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class RDFProcessorTS(RDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def residuals(self, visitor, **kwargs):
        """Here we look for rdf edges that are not in the DCAT-AP.de norm"""

        subject = kwargs['rdf_node']
        kwargs['node_type'] = NT_RESIDUAL

        visitor.scribe.write(
            level='info',
            msg=u'{type} object {obj}: looking for residual properties',
            obj=kwargs['rdf_node'],
            type=kwargs['struct'].rdf_type,
        )
        # Query all predicates
        query = QUERY_P
        # Query the RDF db. Subject is the node we are on
        # is the attribute we like to find in the RDF
        bindings = {
            's': subject,
        }
        results = self.graph.query(query, initBindings=bindings)

        if len(results) > 0:
            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: residual properties found',
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )
        else:
            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: No residual properties found',
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )

        # Find the predicates we have already processed
        field_and_references = kwargs['struct'].fields_and_referenced
        dcat_predicates_values = field_and_references.values()
        dcat_predicates = [i['predicate'] for i in dcat_predicates_values]
        dcat_contained_values = kwargs['struct'].contained.values()
        dcat_contained = [i['predicate'] for i in dcat_contained_values]
        dcat_predicates += dcat_contained

        # Handle the predicates we have missed
        for result in results:
            # if the result is already covered by dcat-ap.de pass
            if result['p'] in dcat_predicates:
                continue
            self.residual(visitor, result, **kwargs)

        visitor.pop_node()

    def residual(self, visitor, predicate_object, **kwargs):
        """Handle on residual"""

        predicate = predicate_object['p']
        rdf_obj = predicate_object['o']

        # If the field is a Literal we simply store it.
        if isinstance(rdf_obj, Literal):
            val = literal2plone(rdf_obj)
            visitor.end_node(predicate, rdf_obj, **kwargs)
        # if not we have to create a sub object recursively
        else:
            params = kwargs.copy()
            params['rdf_node'] = rdf_obj
            node = visitor.end_node(predicate, rdf_obj, **kwargs)
            visitor.push_node(node)
            val = self.residuals(
                visitor,
                **params)
        visitor.scribe.write(
            level='info',
            msg=u'{type} object {obj}: attribute {att}:= {val}',
            val=val,
            att=predicate,
            obj=kwargs['rdf_node'],
            type=kwargs['struct'].rdf_type,
        )

    def checkURI(self, uri, field_name=None):
        """
        To be implemented
        :param uri:
        :param field_name:
        :return:
        """
        return

    def create_dx_obj(
        self,
        visitor,
        struct,
        context,
        rdf_node,
        obj_data,
        title,
    ):
        # check if object should be created
        if not visitor.real_run:
            return None

        # check if the URI of the object is already available as DX object
        if struct.literal_field is not None:
            brains = self.checkURI(rdf_node.toPython(), struct.literal_field)
        else:
            brains = self.checkURI(rdf_node.toPython())

        if len(brains) > 0:
            visitor.scribe.write(
                level='warn',
                msg=u'{type} dxobject {obj} reused from {context}',
                context=brains[0].getURL(),
                obj=rdf_node,
                type=struct.rdf_type,
            )
            return brains[0].getObject()

        # Handle identifier fields
        identifier_fields = handle_identifiers(rdf_node)
        obj_data.update(identifier_fields)

        # Handle not given descriptions to prevent u'None' brains
        desc_found = False
        for desc_field in struct.desc_field:
            if desc_field in obj_data:
                desc_found = True
                break

        if not desc_found:
            for desc_field in struct.desc_field:
                obj_data[desc_field] = None
            obj_data['description'] = None

        # Create an instance of the node as dexterity object
        try:
            obj = content.create(
                context,
                struct.portal_type,
                title=title,
                in_harvester=self.harvester.UID(),
                **obj_data)
        # We are not allowed to create the content here
        except InvalidParameterError:
            # So we try it directly under the harvest
            visitor.scribe.write(
                level='error',
                msg=u'{type} dxobject {obj} created at {context}',
                context=self.harvester.virtual_url_path(),
                obj=rdf_node,
                type=struct.rdf_type,
            )

            obj = content.create(
                self.harvester,
                struct.portal_type,
                title=title,
                in_harvester=self.harvester.UID(),
                **obj_data)

        self.apply_workflow(obj)

        obj.reindexObject()
        visitor.scribe.write(
            level='info',
            msg=u'{type} dxobject {obj} created at {context}',
            context=context.virtual_url_path(),
            obj=rdf_node,
            type=struct.rdf_type,
        )
        return obj

    def crawl(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        """Analyse the RDF structure"""

        # Activate the struct
        struct = target_struct(self.harvester)

        # here we collect the data to generate our DX object
        obj_data = {}

        # set the original URI as rdf_about field:
        obj_data['rdf_about'] = rdf_node

        # Go for the DCAT-AP.de properties of the current node
        self.properties(
            visitor,
            context=context,
            rdf_node=rdf_node,
            struct=struct,
            obj_data=obj_data,
        )

        # # Find the edges that are not included in DCAT-Ap.de
        # self.residuals(
        #     visitor,
        #     context=context,
        #     rdf_node=rdf_node,
        #     struct=struct,
        #     obj_data=obj_data,
        # )

        try:
            # get a title for the dxobject
            title = self.get_title(struct, obj_data)

            # Hack for convention 31: Handle dct_format as literal
            if struct.literal_field is not None:
                if isinstance(title, Literal):
                    lit2dict = self.literal_handler.literal2dict(title)
                    obj_data[struct.literal_field] = lit2dict
                else:
                    obj_data[struct.literal_field] = title

            # create the DX object
            obj = self.create_dx_obj(
                visitor,
                struct,
                context,
                rdf_node,
                obj_data,
                title,
            )
        except RequiredPredicateMissing:
            if context:
                context_url = context.virtual_url_path()
            else:
                context_url = '/'
            visitor.scribe.write(
                level='error',
                msg=u'{type} dxobject {obj} cannot be created at {context}',
                context=context_url,
                obj=rdf_node,
                type=struct.rdf_type,
            )
            obj = None
            title = None

        # deal with the contained objects
        self.contained(
            visitor,
            context=context,
            rdf_node=rdf_node,
            struct=struct,
            obj_data=obj_data,
            obj=obj,
        )

        # end recursion
        node = visitor.pop_node()

        node.title = title

        return obj

    def crawl_dx(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):

        struct = target_struct(context)
        field_and_references = struct.fields_and_referenced
        obj_data = {}

        for field_name, field in field_and_references.items():
            predicate = field['predicate']
            obj_class = field['object']
            params = {
                'field': field,
                'field_name': field_name,
                'struct': target_struct,
            }
            # If the field is a Literal we simply store it.
            if obj_class == StructRDFSLiteral:
                # todo: is None as default correct or should
                # this case be ignored
                obj_data[field_name] = getattr(context, field_name, None)
                visitor.end_node(predicate, obj_class, **params)
            # if not we have to create a sub object recursively
            else:
                node = visitor.end_node(predicate, obj_class, **params)
                visitor.push_node(node)
                sub = self.crawl_dx(
                    visitor,
                    context=context,
                    target_struct=obj_class,
                )
                obj_data[field_name] = sub
            visitor.scribe.write(
                level='info',
                msg=u'{type} DX object {obj}: attribute {att}:= {val}',
                val=obj_data[field_name],
                att=predicate,
                obj=context,
                type=struct.rdf_type,
            )

        node = visitor.pop_node()
        # todo: check if this is correct
        if context:
            node.title = context.Title()
        else:
            node.title = ''
