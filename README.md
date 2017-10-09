FTS Manager
===========

A tool used to manage the FTS Seminar Series at Cardiff University's School of
Computer Science and Informatics.

## Installation
To install this package you will first have to install the dependencies recorded
in requirements.txt. These dependencies can be installed through
`pip -r requirements.txt`, note that `pyldap` has several external dependencies
that need to be installed prior to install -- libsasl2, libldap2, and libssl
(and associated development files) . These external dependencies can be
installed through your distributions package manager, for example using `sudo apt
install libsasl2-dev libldap2-dev libssl-dev`.

Please examine `FTSManager/FTSManager/settings.py`, ensuring that database 
settings are correct, that email settings are correct, and that STATIC_ROOT is 
set to a location that your web server is serving as /static/. Additionally, the
hostname of the server needs to be added to the `ALLOWED_HOSTS` list.

Once dependencies are installed, and settings have been correctly defined
(contained in the `FTSManager/settings.py` file) the database can be initialised
by running `python manage.py migrate`, and static files can be collected for 
serving by running `python manage.py collectstatic`. 

FTS-Manager can be run through with the command `python manage.py runserver` --
if everything is working as it should be, then visiting `http://localhost:8000`
in a web browser should serve you with a blank FTS manager home page.

The preferred method for serving FTS-Manager in production is using wsgi, using
a server container such as uWSGI. Django provides a wsgi callable, accessible
through `FTSManager.wsgi`. An example uWSGI command for FTS-Manager would be:

`uwsgi --socket 127.0.0.1:31337 --chdir /path/to/folder/containing/this/file/FTSManager --wsgi-file FTSManager/wsgi.py --master --threads 8`

(example chdir path is `/home/user/FTS-Manager/FTSManager` -- note that the
FTSManager directory contains a subdirectory of the same name)

Having set up uwsgi, nginx/apache should be set up to proxy requests to
127.0.0.1:31337.

In order to populate FTS-Manager with LDAP users , please run
`python manage.py sync_ldap`. This will pre-populate all users of type
"Research Student" into Django's user database, allowing autocompletion of users
who have not yet logged in.

The final step is to configure cron to execute FTS-Manager periodic tasks.
This can be done by running the command `python manage.py installtasks`.
This will install a nightly cron to sync ldap users, and a minutely cron to send
reminder emails (where necessary).


## Tools
In order to add users that are not marked as a "Research Student" in LDAP,
the management commmand `python mange.py add_user <username>` can be used. 
Note that any user in the LDAP server is able to log in to FTS-Manager, and
`add_user` is only needed for adding talks on behalf of users that have never
signed in.

