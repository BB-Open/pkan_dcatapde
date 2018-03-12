# -*- coding: utf-8 -*-
"""Remembering things"""
from datetime import datetime
from pkan.dcatapde.structure.sparql import namespace_manager
from pkan.dcatapde.structure.structure import StructRDFSLiteral


class Scribe(object):
    """Instance to write things to and to retrieve them later"""

    def __init__(self):
        self.data = []

    def write(self, msg=None, level=None, **data):
        self.data.append({
            'time': datetime.now(),
            'log': msg,
            'level': level,
            'data': data,
        })

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

# Node types
NT_NORMAL = 'Normal'
NT_SPARQL = 'SPARQL'
NT_DX_DEFAULT = 'DX default'
NT_DX_LINK = 'DX link'

NODETYPE2SHAPE = {
    NT_NORMAL: 'rectangle',
    NT_SPARQL: 'roundrectangle',
    NT_DX_DEFAULT: 'hexagon',
    NT_DX_LINK: 'octagon',
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
    def short_id(self):
        result = namespace_manager.normalizeUri(self.id)
        return result

    @property
    def short_title(self):
        result = namespace_manager.normalizeUri(self.title)
        return result


class Node(Base):
    """Represents a node"""

    position = None

    def __init__(
        self,
        id,
        structure,
        type=NT_NORMAL,
        status=NS_NORMAL,
        title=None,
        position=None,
        parent=None,
    ):
        self.id = id
        self.structure = structure
        if not title:
            self.title = self.id
        self.type = type
        self.status = {}
        self.status[status] = status
        self.position = position
        self.parent = parent
        self.next_child_pos = 0

    @property
    def child_pos(self):
        self.next_child_pos += 20
        return {'x': 10, 'y': self.next_child_pos}

    def to_cytoscape(self):
        result = {}
        result['group'] = 'nodes'

        data = {}
        data['id'] = self.short_id

        data['pkwidth'] = str(len(data['id']) * 10)

        status = NS_NORMAL
        # Determine the Node status
        for ns in NODESTATUSORDER:
            if ns in self.status:
                status = ns
        data['pkbackgroundcolor'] = NODESTATUS2COLOR[status]

        data['pkshape'] = NODETYPE2SHAPE[self.type]

        if self.parent:
            data['parent'] = self.parent.short_id
            data['pkvalign'] = 'center'
        else:
            data['pkvalign'] = 'top'

        if self.position:
            result['position'] = self.position

        result['data'] = data
        return result


class Edge(Base):
    """Represents an edge"""
    counter = 0

    def __init__(self, source, target, title=None):
        self.id = self.counter
        Edge.counter += 1
        if title:
            self.title = title
        else:
            self.title = self.id
        self.source = source
        self.target = target

    def to_cytoscape(self):
        data = {}
        data['id'] = self.short_id
        data['source'] = self.source.short_id
        data['target'] = self.target.short_id
        data['group'] = 'edges'
        data['label'] = self.short_title
        classes = 'autorotate'
        result = {
            'data': data,
            'classes': classes,
        }
        return result


class BaseVisitor(object):
    """Base visitor. Contains a graph consisting of nodes and edges
    as well as a scribe to generate meaningfull logs"""

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.scribe = Scribe()
        self.node_stack = []

    def pop_node(self):
        return self.node_stack.pop()

    def push_node(self, node):
        self.nodes[node.id] = node
        self.node_stack.append(node)

    def add_node(self, node):
        self.nodes[node.id] = node
        return node

    def end_node(self, **kwargs):
        field = kwargs['field']
        if 'status' in kwargs:
            status = kwargs['status']
        else:
            status = NS_NORMAL
        predicate = field['predicate']
        obj = field['object']
        if obj == StructRDFSLiteral:
            parent = self.node_stack[-1]
            node = Node(
                predicate,
                predicate,
                status=status,
                parent=parent,
                position=parent.child_pos,
            )
        else:
            node = Node(
                obj.rdf_type,
                obj.rdf_type,
                status=status,
            )
            if self.node_stack:
                edge = Edge(self.node_stack[-1], node, title=predicate)
                self.add_edge(edge)

        self.add_node(node)
        return node

    def add_edge(self, edge):
        self.edges[edge.id] = edge
        return edge

    def get_node(self, id):
        return self.nodes[id]

    def get_edge(self, id):
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
        self.edge_uids = {}
        super(DCATVisitor, self).__init__()

    def get_entity_mapping(self, source, predicate):
        return None

    def add_node(self, node):
        # check if we had such a node already
        if node.id in self.nodes:
            self.nodes[node.id].status.update(node.status)
        else:
            super(DCATVisitor, self).add_node(node)
        return node

    def add_edge(self, edge):
        # check if we had such an edge already
        uid = '_'.join([
            edge.source.id,
            edge.target.id,
            edge.title,
        ])
        if uid in self.edge_uids:
            return
        super(DCATVisitor, self).add_edge(edge)

        self.edge_uids[uid] = 1

        return edge

    def to_cytoscape(self):
        result = []
        for node in self.nodes.values():
            result.append(node.to_cytoscape())

        for edge in self.edges.values():
            result.append(edge.to_cytoscape())

        return result


class InputVisitor(BaseVisitor):
    """Vistor for Input data"""
