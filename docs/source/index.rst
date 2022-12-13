Welcome to bravia's documentation!
==================================

.. _What is it?:

What is it?
===========

bravia is a python module for Sony Bravia Professional Displays running Android.
See `Sony Developer docs <https://pro-bravia.sony.net/develop/integrate/ip-control/index.html>`_
for more details.

.. _What can it do?:

What can it do?
===============

bravia will let you control some functions of the display via an API. Some functions require
pre-shared key configuration on the display. They are documented in the developer docs reference
in the :ref:`What is it?` section.

Quickstart
==========

Make a call to the display API for all services.

    >>> from bravia import Bravia
    >>> b = Bravia(ip='192.168.1.25')
    >>> b.api_info()

This will show the API for each service available on the display. Use this developer docs referenced in
:ref:`What is it?` to see more functionality.

Index
=====

.. toctree::
   :titlesonly:

   bravia
