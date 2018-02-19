=============
pkan.dcatapde
=============

PKAN (Plone Knowledge And Norms) is an applikation to create, import and export semantic web information
with a strong focus on the german `DCAT-AP.de <dact-ap.de>`_ metadata norm governing the operation.

The semantic web gives us unlimited possibilities to express knowledge. Being founded on boundless possibilities is a nice feature but alone it does
not suffice to make a new technology usefull. Although people use natural language to express things of their daily live the human kind has prosper
not solely by having the feature of universal languages. Inventions of formal descriptions like ledger, aritmethic tabular, formulars, spreadsheets,
realtional database, programing language are the robust building blocks of our culture. And these formal descriptions have shaped our mind and our thinking.

The part of humanity which is formalized the most is (beside pure mathematics :-) ) the administration. The aim of PKAN is to help the administration to
make there first steps into the new semantic web technology and have a clean and successful start.

The german metadata standard DCAT-AP.de is based on DCAT-AP the european standard, which in turn is based in the long run on
the `DCAT (Data Catalog Vocabulary) standard <https://www.w3.org/TR/vocab-dcat/>`_. Administrative processes have convoluted the initial four entities of
DCAT to become 22 entities in DCAT-AP.de. Now the
`UML diagram of DACT-AP.de <http://www.dcat-ap.de/def/dcatde/1_0/uml/modelio.pdf>`_
looks to persons in administration more like the subway chart of Tokio than like their beloved spreadsheets, ledgers or catalogues. We like to help those persons.

- PKAN comes with modern web formulars for all 22 entities to create metadata that are already DCAT-AP.de when typed into the formular
- PKAN imports (harvest) arbitrary RDF-based data sources and

   - transform them into valid DCAT-AP.de entities
   - edit and enrich the entities
   - and finally export (marshall) the entities to an upstream semantic web server (govdata.de in germany)

PKAN is programmed as a set of Add-Ons for the  `Plone CMS <https://plone.org>`_. Plone has a proved and tested codebase and a quite successful history not
only as content management system. Plone comes with lots of batteries included like persistent searches, a workflow engine and the revisioning of documents.
Utilizing these Plone features nearly all requirementes of DCAT-AP.de that are not directly visible in the naked UML-Diagram can be solved with a minimum of
programming.

Plone does not know much about the semantic web. The semantic web part of the PKAN application is based on the RDFlib python library.  Utilizing RDFlib together
with a PostgreSQL database server we added a complete triple store to PKAN inclusive SPARQL queries and endpoints.



.. only:: html

  Contents
  ========

.. toctree::
   :maxdepth: 2

   Overview <overview>
   Installation <install>
   Configuration <configuration/index>
   Content Types <content_types/index>
   Development <develop>


Contribute
==========

- Issue Tracker: https://github.com/BB-Open/pkan.dcatapde/issues
- Source Code: https://github.com/BB-Open/pkan.dcatapde
- Documentation: https://pkandcatapde.readthedocs.io


Support
=======

If you are having issues, please let us know.
We have a issue tracker located at: https://github.com/BB-Open/pkan.dcatapde/issues


License
=======

The project is licensed under the GPLv2.
