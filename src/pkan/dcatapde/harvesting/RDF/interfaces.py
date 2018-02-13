# -*- coding: utf-8 -*-
from zope.interface import Interface


class ICrawler(Interface):
    """
    Base Interface for Data-Crawler
    """


class IRDF(ICrawler):
    """
    Interface for RDF-Crawler
    """
