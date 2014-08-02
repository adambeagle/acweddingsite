============
Installation
============

*Please note that this document assumes basic familiarity with 
Django, pip, and virtualenv.*

Dependencies
============

This project was developed for, and only tested with, Python 3.3. 
It has been designed to work with ``pip`` and ``virtualenv``. 
A requirements.txt file is included at the repository root that 
delineates the dependencies that can be installed via ``pip``.

Note: make_thumbnails.py and Pillow
-----------------------------------

The script ``util/make_thumbnails.py`` requires the python library 
Pillow (or the older PIL), which has its own dependency issues depending
on platform (on my Xubuntu system, it required the installation of 
``python-imaging``). Due to the size of these packages and the 
non-essential nature of ``make_thumbnails.py``, Pillow is not 
included in ``requirements.txt``.

Instructions
============

0. Optionally (but preferably), create a virtualenv with Python 3.3 as the default Python for use with the project.

1. From the root directory of the repository, ``pip install -r requirements.txt`` will install all necessary dependencies (Django, etc.).

2. The Django settings as given expect environment variables named  ``SECRET_KEY``, ``DB_USERNAME``, ``DB_PASSWORD``, ``EMAIL_HOST_USER``, and ``EMAIL_HOST_PASSWORD``. Either set these environment variables locally or hardcode values into the settings (located in ``acwedding/acwedding/settings/``). Consider using ``virtualenvwrapper``'s ``postactivate`` and ``predeactivate`` scripts to set/unset the environment variables automatically. Additionally, ``CONTACT_EMAIL`` and ``DOMAIN`` environment variables are expected by core.forms.ContactForm.

3. Configure the ``DATABASES`` setting in ``local.py`` in the settings directory. Note the project has only been tested with PostgreSQL.

4. ``syncdb``

5. Load fixtures from ``acwedding/fixtures`` using ``python manage.py loaddata <file>``. *(Fixtures are not included in the github repo).*

6. The site should now be available to view at ``localhost:8000`` after ``runserver`` is run. 
