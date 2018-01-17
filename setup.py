# -*- coding: utf-8 -*-
"""Installer for the pkan.dcatapde package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='pkan.dcatapde',
    version='1.0a1',
    description="DCAT-AP.de content types for plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Dr. Volker Jaenisch',
    author_email='volker.jaenisch@inqbus.de',
    url='https://pypi.python.org/pypi/pkan.dcatapde',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['pkan'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'chardet',
        'plone.api',
        'plone.app.dexterity',
        'plone.formwidget.relateditems',
        'Products.GenericSetup >= 1.8.2',
        'ps.zope.i18nfield >= 0.5',
        'surf',
        'z3c.jbot',
        'zope.app.content',
        'collective.z3cform.datagridfield',
        'requests'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
