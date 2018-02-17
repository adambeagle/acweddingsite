Purpose
-------

This repository contains the source code (and static resources, etc.) for the website built for my wedding (May 2015). It was built using Django 1.6. The site is no longer live, but I'll leave this repository here for posterity. 


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

:/tourisminfo: Django app that includes an index and detail pages for attractions, dining, and lodging options.

:/templates: Templates from all apps are in this directory. The directory structure and naming patterns are modeled after those found in "Two Scoops of Django" 12.2.1.

Legal
-----

See ``docs/LICENSE.txt`` for license information. 
