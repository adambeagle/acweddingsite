Purpose
-------

This repository contains the source code (and static resources, etc.) for a website being built for my upcoming wedding. It is built using Django 1.6. I hope it can serve as a useful example to others who want to build a small Django-powered site. I'm making every effort to follow any best practices of which I'm aware, in particular many described in the book "Two Scoops of Django."

The site is currently somewhere in the mid-to-late stage of local development. The target deployment date is no later than August 2014.


Documentation
-------------

Project-wide documentation is located in the ``docs/`` directory at the repository root. Documentation for individual modules is found in their respective files.


Installation
------------

See ``docs/installation.rst``


Layout
------

Repository root
^^^^^^^^^^^^^^^
:/docs: Project-wide documentation lives here.

:/acwedding: The Django project root directory.

:/util: Utility scripts that are independent of Django.

:requirements: Requirements.txt lists required python packages and their versions. Useful in conjunction with ``pip.`` See ``/docs/installation.rst``

Django Project Directory (/acwedding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:/acwedding: Configuration for the entire project. The root urlconfs and Django settings are here.

:/core: Django app for the core pages and functionality of the site. 

:/faq: Django app for the FAQ page. 

:/googlemaps: Django app that facilitates embedding Google maps (via Google Maps JavaScript API v3) into pages. Maps can be simple maps with a few markers or more elaborate with animated markers and info windows for each marker.

:/templates: Templates from all apps are in this directory. The directory structure and naming patterns are modeled after those found in "Two Scoops of Django" 12.2.1.


Legal
-----

See ``docs/LICENSE.txt`` for license information. 
