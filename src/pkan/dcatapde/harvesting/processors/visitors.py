# -*- coding: utf-8 -*-
"""Remembering things"""
from datetime import datetime
from pkan.dcatapde.structure.sparql import namespace_manager
from pkan.dcatapde.structure.structure import StructRDFSLiteral
# from plone.api.portal import translate
from rdflib import URIRef

import cgi
import html
import logging


logger = logging.getLogger('Plone')


LEVEL_COLOR = {
    'info': 'green',
    'warn': 'orange',
    'error': 'red',
}

COLOR_MSG = u'<font color={color}>{msg}</font><div>{link}</div>'


def short(uri):
    """Shorten URI the ns-prefix and class"""
    result = namespace_manager.normalizeUri(uri)
    return result


class Scribe(object):
    """Instance to write things to and to retrieve them later"""

    def __init__(self):
        self.data = []
        self.formatted_data = []

    def write(self, msg=None, level=None, **data):
        entry = {
            'time': datetime.now(),
            'log': msg,
            'level': level,
            'data': data,
        }
        self.data.append(entry)
        self.log_entry(entry, level)

    def log_entry(self, entry, level):
        res = self.format_entry(entry)
        if res is None:
            return
        msg, entry = res
        self.formatted_data.append([msg, entry])
        if level == 'info':
            logger.info(msg=msg)
        elif level == 'error':
            logger.info(msg='ERROR: ' + msg)
        elif level == 'warn':
            logger.info(msg='WARN: ' + msg)
        else:
            raise AttributeError
        # Todo: Logger must be configured to write
        #  console even if run without plone

    def read(self):
        for entry in self.data:
            try:
                msg = entry['log'].format(
                    time=entry['time'],
                    level=entry['level'],
                    **entry['data'])
            except KeyError:
                pass
            yield {'msg': msg, 'data': entry['data']}

    def format_entry(self, entry):
        new_entry = entry.copy()
        data = entry['data']
        for item in data:
            if isinstance(data[item], URIRef):
                new_entry['data'][item] = short(data[item])

        # deal with log lines that are multiline like traces
        if isinstance(entry['log'], list):
            for line in entry['log']:
                try:
                    msg_trans = line
                    msg = str(entry['time']) + ': ' + msg_trans.format(
                        time=entry['time'],
                        level=entry['level'],
                        **new_entry['data'])
                    return msg, new_entry
                except KeyError:
                    pass
        else:
            try:
                msg_trans = str(entry['log'])
                msg = str(entry['time']) + ': ' + msg_trans.format(
                    time=entry['time'],
                    level=entry['level'],
                    **new_entry['data'])
                return msg, new_entry
            except KeyError:
                pass
            except IndexError:
                pass
            except ValueError:
                pass

    def html_log(self):
        result = []
        for msg, entry in self.formatted_data:
            try:
                html_msg = cgi.escape(msg)
            except AttributeError:
                html_msg = html.escape(msg)
            link = u'<a class="context pat-plone-modal" ' \
                   u'target="_blank" href="{uri}">Modify</a>'
            color = LEVEL_COLOR[entry['level']]
            color_msg = u'<font face="monospace" color={color}>{level}: {msg}</font>'
            log_line = color_msg.format(
                color=color,
                level=entry['level'],
                msg=html_msg,
                link=link.format(
                    uri=u'http://localhost:8080/Plone6/harvester_preview',
                ),
            )
            result.append(log_line.replace('\n', '<br/>'))
        return result


# Node types
NT_NORMAL = 'Normal'
NT_DEFAULT = 'Default'
NT_SPARQL = 'SPARQL'
NT_DX_DEFAULT = 'DX default'
NT_DX_LINK = 'DX link'
NT_RESIDUAL = 'Residual'

NODETYPE2SHAPE = {
    NT_NORMAL: 'rectangle',
    NT_DEFAULT: 'roundrectangle',
    NT_DX_DEFAULT: 'roundrectangle',
    NT_DX_LINK: 'roundrectangle',
    NT_SPARQL: 'roundrectangle',
    NT_RESIDUAL: 'rectangle',
}

NODETYPE2BORDERCOLOR = {
    NT_NORMAL: '#000000',
    NT_DEFAULT: '#000000',
    NT_DX_DEFAULT: '#000000',
    NT_DX_LINK: '#000000',
    NT_SPARQL: '#000000',
    NT_RESIDUAL: '#FF0000',
}

NODETYPE2OPACITY = {
    NT_NORMAL: 1,
    NT_DEFAULT: 1,
    NT_DX_DEFAULT: 1,
    NT_DX_LINK: 1,
    NT_SPARQL: 1,
    NT_RESIDUAL: 0.3,
}

# Node status
NS_NORMAL = 'Normal'
NS_WARNING = 'Warning'
NS_ERROR = 'Error'

# Order od node status
NODESTATUSORDER = [NS_NORMAL, NS_WARNING, NS_ERROR]

NODESTATUS2COLOR = {
    NS_NORMAL: '#00FF00',
    NS_WARNING: '#F7C80D',
    NS_ERROR: '#FF0000',
}

# Node importance (mandatory, recommended, optional)
# Node states
NI_MANDATORY = 'Mandatory'
NI_RECOMMENDED = 'Recommended'
NI_OPTIONAL = 'Optional'

NODETYPE2CSSCLASS = {
    NI_MANDATORY: 'node_importance_mandatory',
    NI_RECOMMENDED: 'node_importance_recommended',
    NI_OPTIONAL: 'node_importance_optional',
}


class Base(object):
    """Bese fro nodes and edges"""

    id = None
    title = None

    @property
    def short_title(self):
        result = namespace_manager.normalizeUri(self.title)
        return result

    def short(self, uri):
        """Shorten URI the ns-prefix and class"""
        result = namespace_manager.normalizeUri(uri)
        return result


class Node(Base):
    """Represents a node"""

    position = None
    counter = 0

    def __init__(
        self,
        structure,
        node_type=NT_NORMAL,
        status=NS_NORMAL,
        title=None,
        position=None,
        parent=None,
        duplicate=False,
    ):
        self.id = 'n:' + str(self.counter)
        Node.counter += 1

        self.structure = structure
        self.title = title
        self.node_type = node_type
        self.status = {}
        self.status[status] = status
        self.position = position
        self.parent = parent
        self.next_child_pos = 0
        self.duplicate = duplicate

    @property
    def child_pos(self):
        self.next_child_pos += 20
        return {'x': 10, 'y': self.next_child_pos}

    def to_cytoscape(self):
        result = {}
        result['group'] = 'nodes'

        data = {}
        data['id'] = self.id
        if self.title:
            rdf_type = self.structure.rdf_type
            short_rdf_type = self.short(rdf_type)
            data['title'] = short_rdf_type + ':\n' + self.short_title
        elif isinstance(self.structure, URIRef):
            rdf_type = self.structure
            data['title'] = self.short(rdf_type)
        elif isinstance(self.structure, str):
            data['title'] = self.structure
        else:
            rdf_type = self.structure.rdf_type
            data['title'] = self.short(rdf_type)

        data['pkwidth'] = str(len(data['title']) * 10)

        status = NS_NORMAL
        # Determine the Node status
        for ns in NODESTATUSORDER:
            if ns in self.status:
                status = ns
        data['pkbackgroundcolor'] = NODESTATUS2COLOR[status]

        data['pkshape'] = NODETYPE2SHAPE[self.node_type]
        data['pkbordercolor'] = NODETYPE2BORDERCOLOR[self.node_type]
        data['pkopacity'] = NODETYPE2OPACITY[self.node_type]

        if self.parent:
            data['parent'] = self.parent.id
            data['pkvalign'] = 'center'
            data['pkfontsize'] = '20pt'
        else:
            data['pkvalign'] = 'top'
            data['pkfontsize'] = '25pt'

        if self.position:
            result['position'] = self.position

        if self.duplicate:
            result['classes'] = 'duplicate'

        result['data'] = data
        return result


class Edge(Base):
    """Represents an edge"""
    counter = 0

    def __init__(self, source, target, title=None, duplicate=False):
        self.id = 'e:' + str(self.counter)
        Edge.counter += 1
        if title:
            self.title = title
        else:
            self.title = self.id
        self.source = source
        self.target = target
        self.duplicate = duplicate

    def to_cytoscape(self):
        data = {}
        data['id'] = self.id
        data['source'] = self.source.id
        data['target'] = self.target.id
        data['group'] = 'edges'
        data['label'] = self.short_title
        classes = 'autorotate'
        if self.duplicate:
            classes += ' duplicate'
        result = {
            'data': data,
            'classes': classes,
        }
        return result


class BaseVisitor(object):
    """Base visitor. Contains a graph consisting of nodes and edges
    as well as a scribe to generate meaningfull logs"""
    real_run = False

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.scribe = Scribe()
        self.node_stack = []

    def short(self, uri):
        """Shorten URI the ns-prefix and class"""
        result = namespace_manager.normalizeUri(uri)
        return result

    def pop_node(self):
        return self.node_stack.pop()

    def push_node(self, node):
        self.nodes[node.id] = node
        self.node_stack.append(node)

    def add_node(self, node):
        self.nodes[node.id] = node
        return node

    def end_node(self, predicate, obj, **kwargs):
        """Generate an edge and an Node"""
        # From the field we get the predicate and the object
        #        field = kwargs['field']
        #        predicate = field['predicate']
        #        obj = field['object']
        # the status of the node
        if 'status' in kwargs:
            status = kwargs['status']
        else:
            status = NS_NORMAL
        # the type of the node
        if 'node_type' in kwargs:
            node_type = kwargs['node_type']
        else:
            node_type = NT_NORMAL

        # Deal with duplicate Nodes
        is_duplicate = False
        if 'duplicate' in kwargs:
            is_duplicate = kwargs['duplicate']

        # If we deal with a literal build a composite node
        # and omit the edge
        # aka give a parent node. The parent node is found on the stack
        # also we derive the position of the childnode
        if obj == StructRDFSLiteral:
            try:
                parent = self.node_stack[-1]
            except IndexError:
                node = Node(
                    predicate,
                    status=status,
                    duplicate=is_duplicate,
                    node_type=node_type,
                )
            else:
                node = Node(
                    predicate,
                    status=status,
                    parent=parent,
                    position=parent.child_pos,
                    duplicate=is_duplicate,
                    node_type=node_type,
                )
        else:
            # not a literal node so we build a node ..
            node = Node(
                obj,
                status=status,
                duplicate=is_duplicate,
                node_type=node_type,
            )
            # .. and an edge
            if self.node_stack:
                edge = Edge(
                    self.node_stack[-1],
                    node,
                    title=predicate,
                    duplicate=is_duplicate,
                )
                self.add_edge(edge)

        # in both cases we have to memorize the node
        self.add_node(node)
        return node

    def add_edge(self, edge):
        """Simply memorize the edge"""
        self.edges[edge.id] = edge
        return edge

    def get_node(self, id):
        """Return a node by id"""
        return self.nodes[id]

    def get_edge(self, id):
        """Return an edge by id"""
        return self.edges[id]


class DCATVisitor(BaseVisitor):
    """Visitor to construct a DCATAPDE Graph diagram.
    Node colors indicate the node status (Good, bad, ugly).
    The node shape indicates the type
        Normal:Rectangle,
        SPARQL:RoundetRectangle,
        DXDefault:Hexagon,
        DXLink:Octagon,
        """

    def __init__(self):
        # These dicts are the store for duplicate detection of
        # nodes and edges
        self.edge_uids = {}
        self.node_uids = {}
        super(DCATVisitor, self).__init__()

    def get_entity_mapping(self, source, predicate):
        """Todo this call should give the entity mapping for the node"""
        return None

    def end_node(self, predicate, obj, **kwargs):
        """Determine if the node was already seen"""
        # Find subject, predicate, object
        struct = kwargs['struct']
        subject = self.short(struct.rdf_type)
        predicate = self.short(predicate)
        short_obj = self.short(obj)
        # build a uid for the triple
        uid = '_'.join([
            subject,
            predicate,
            short_obj,
        ])
        # check if triple already has been seen then mark
        # the edge and node as duplicates
        if uid in self.node_uids:
            return super(DCATVisitor, self).end_node(
                predicate,
                obj,
                duplicate=True,
                **kwargs)
        else:
            return super(DCATVisitor, self).end_node(
                predicate,
                obj,
                **kwargs)

    def to_cytoscape(self):
        nodes = []
        edges = []
        for node in self.nodes.values():
            nodes.append(node.to_cytoscape())

        for edge in self.edges.values():
            edges.append(edge.to_cytoscape())

        result = {'elements': {'nodes': nodes, 'edges': edges}}

        return result


class InputVisitor(BaseVisitor):
    """Vistor for Input data"""


class RealRunVisitor(BaseVisitor):
    """Vistor for Input data"""

    real_run = True
