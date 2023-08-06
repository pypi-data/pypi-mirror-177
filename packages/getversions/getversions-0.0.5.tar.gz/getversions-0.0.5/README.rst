getversions
===========

Get the versions of a package available in the repository via pip, and the installed
version.

Installation
------------

.. code-block:: shell

  pip install getversions

Usage
-----

Print Available and Installed Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

  python -m getversions.getversions package_name

For instance,

.. code-block:: shell

  python -m getversions.getversions black

would produce output similar to

.. code-block:: shell

  *22.10.0
  22.8.0
  22.6.0
  22.3.0
  22.1.0

where `black 22.10.0` is installed for the current Python interpreter.

Check Installed Version Available in Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the installed version of the package for the current interpreter is not available
in the repository, the command below will have an exit code of 0, in which case you
might want to upload the installed version to the repository.

.. code-block:: shell

  python -m getversions.newinstalledversion package_name
