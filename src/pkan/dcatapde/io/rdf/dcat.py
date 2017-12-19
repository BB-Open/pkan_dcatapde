from pkan.dcatapde.io.rdf.dexterity import Dexterity2Surf
from pkan.dcatapde.content.foafagent import IFoafagent
from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde.io.rdf.interfaces import ISurfSession
from zope.component import adapts
import surf

class FOAF2Surf(Dexterity2Surf):
    """ Dexterity implementation of the Object2Surf
    """

    adapts(IFoafagent, ISurfSession)


    _whitelist = ['name']

    _namespace = surf.ns.FOAF   # stores the namespace for this resource
    _prefix = 'foaf'


class Catalog2Surf(Dexterity2Surf):
    """ Dexterity implementation of the Object2Surf
    """

    adapts(ICatalog, ISurfSession)


    _whitelist = ['title',
                  'description',
                  'publisher',
                  'add_title',
                  'add_description',
                  ]

    _namespace = surf.ns.DCAT   # stores the namespace for this resource
    _prefix = 'dcat'
