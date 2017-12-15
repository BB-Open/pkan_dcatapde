""" Interfaces """

from zope.interface import Attribute, Interface


class ISurfSession(Interface):
    """The surf.Session objects"""


class IObject2Surf(Interface):
    """ An object that writes surf info into a ISurfSession
    """

    def write():
        """Add the surf resource info into the session """


class IGenericObject2Surf(IObject2Surf):
    """ An implementation of IObject2Surf

    This interface is only used to describe the GenericObject2Surf
    class; The IObject2Surf interface should be used as adapter interface
    """

    resource = Attribute(u"A surf resource that is written into the sesion")
    namespace = Attribute(u"The namespace that is attached to the resource")
    subject = Attribute(u"The subject (URI) of the resource")
    prefix = Attribute(u"The subject (URI) of the resource")
    portalType = Attribute(u"The portal type of the context, "
                           u"will be used as resource class")
    rdfId = Attribute(u"The Id of the resource")

    def modify_resource(resource, *args, **kwds):
        """Override to modify the resource and return a new one
        """


class ISurfResourceModifier(Interface):
    """Plugins that can modify the saved resource for a given context
    """

    def run(resource):
        """Gets the rdf resource as argument, to allow it to be changed in place
        """


class IField2Surf(Interface):
    """
    """
    exportable = Attribute("Is this field exportable to RDF?")

    def value(context):
        """ Returns the value in format understandable by SURF """


class IValue2Surf(Interface):
    """Transform a python value in a format suitable for Surf
    """

    def __call__(*args, **kwds):
        """Return a value suitable to be assigned as a value to an
        rdf resource attribute
        """


class IFieldDefinition2Surf(IGenericObject2Surf):
    """A three-way adapter to get rdf information from field definitions
    """
