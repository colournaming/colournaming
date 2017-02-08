===============
colornaming.net
===============

This is the code for the colornaming.net website and experiment.


Testing
=======

A local instance of the app can be launched using Docker Compose::

    docker-compose build
    docker-compose up -d postgres
    docker-compose run --rm web initdb
    docker-compose run --rm web import_centroids English en /path/to/dataset_en.csv
    docker-compose up web

Under Linux the app can now be accessed at `localhost:5000 <http://localhost:5000>`_.
If you're using docker-machine (e.g. on OS X) then run ``docker-machine ip`` to
get the machine IP address and browse to port 5000 on that address.

The database can be reinitialized by running::

    docker-compose run --rm web dropdb
    docker-compose run --rm web initdb

Additional dataset can be added by running e.g.::

    docker-compose run --rm web import_centroids Francais fr /path/to/dataset_fr.csv

To stop the test instance run::

    docker-compose down


Translation
===========

See the `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_ website for
information on adding translations.  Check the pages in
`colournaming/templates` for an example of how to use translated text.
