# -*- coding: utf-8 -*-
""" extras """

from .interfaces import ISurfResourceModifier
from .modifiers import BaseFileModifier
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IImage
from Products.CMFPlone import log
from zope.component import adapter
from zope.interface import implementer

import sys


try:
    from collective.cover.interfaces import ICover
except ImportError:
    from zope.interface import Interface

    class ICover(Interface):
        """ Dummy replacement interface
        """


@implementer(ISurfResourceModifier)
@adapter(ICover)
class CoverTilesModifier(object):
    """Adds tiles information to rdf resources
    """

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        uids = self.context.list_tiles()
        value = ''

        for uid in uids:
            tile = self.context.get_tile(uid)
            text = tile.data.get('text', None)

            if text:
                # convert to unicode

                if not isinstance(text.output, unicode):
                    value += unicode(text.output, 'utf-8')
                else:
                    value += text.output

        if value:
            try:
                setattr(resource, '{0}_{1}'.format('eea', 'cover_tiles'),
                        [value])
            except Exception:
                log.log(
                    'RDF marshaller error for context[tiles]'
                    '"{0}[: \n{1}: {2}"'.format(
                        self.context.absolute_url(),
                        sys.exc_info()[0], sys.exc_info()[1]
                    ),
                    severity=log.logging.WARN
                )

        return resource


@adapter(IImage)
class ImageModifier(BaseFileModifier):
    """ ImageModifier """

    field = 'image'


@adapter(IFile)
class FileModifier(BaseFileModifier):
    """ FileModifier """

    field = 'file'
