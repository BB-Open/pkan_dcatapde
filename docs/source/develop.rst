==============
How To Develop
==============

This section should give developers a holding hand on how to contribute and work with the repository.


Coding Style
============

Please follow the official `Plone Coding Style Guides <https://docs.plone.org/develop/styleguide/index.html>`_.


Local Development Environment
=============================

`pkan.dcatapde` ships with a `Pipfile`.
To use it, you need to install `pipenv`.
Please follow the `installation instructions for pipenv <https://docs.pipenv.org/install/>`_ on how to do this for your environment.

Use `pipenv` to create your local development environment.

.. code-block:: console

  $ pipenv install --dev

This will create a virtual environment for this project and install all the development dependencies for you.

Next, activate your virtual enviroment:

.. code-block:: console

  $ pipenv shell


Now you can use buildout to set up your Plone development setup:

.. code-block:: console

  $ buildout


Translations
============

Translations are key to every software project.
We use `Transifex <https://www.transifex.com/>`_ to manage all translations.

To update translations from Transifex, please run:

.. code-block:: console

   $ tx pull -af

This will override the local translation files with the online versions.
Double check for any errors before you commit the changes.

To update the message catalog, first collect all new message id's:

.. code-block:: console

   $ ./bin/rebuild_i18n.sh

If new message id's have been collected, you can push the message catalog to Transifex:

.. code-block:: console

   $ tx push -s

After pushing a message catalog source it is best practice to update the translation files:

.. code-block:: console

   $ tx pull -af
