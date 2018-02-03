# -*- coding: utf-8 -*-
"""Installer for the pkan.dcatapde package."""

from setuptools import find_packages
from setuptools import setup

version = '0.1.dev0'
description = 'DCAT-AP.de content types for Plone.'
long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
    'setuptools',
    # -*- Extra requirements: -*-
    'chardet',
    'collective.z3cform.datagridfield >= 1.3.0',
    'plone.api',
    'plone.app.dexterity',
    'plone.formwidget.relateditems >= 0.2',
    'Products.GenericSetup >= 1.8.2',
    'ps.zope.i18nfield >= 0.7',
    'requests',
    'surf',
    'rdflib',
    'rdflib-sqlalchemy',
    'vkbeautify',
    'z3c.jbot',
    'zope.app.content',
    ],

test_requires = [
    'plone.app.contenttypes',
    'plone.app.robotframework[debug]',
    'plone.app.testing',
    'robotframework-selenium2screenshots',
]

testfixture_requires = [
]

setup(
    name='pkan.dcatapde',
    version=version,
    description=description,
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='Python Plone',
    author='Dr. Volker Jaenisch',
    author_email='volker.jaenisch@inqbus.de',
    url='https://github.com/inqbus/pkan.dcatapde',
    download_url='https://pypi.python.org/pypi/pkan.dcatapde',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['pkan'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
        'testfixture': testfixture_requires,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
