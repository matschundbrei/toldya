# Toldya

This is the recreation of an app that one of my former coworkers [Oli Zimpasser](https://github.com/oglimmer) made.
The source of the  [app called 'toldyouso' is still available here](https://github.com/oglimmer/toldyouso).

The formerly hosted variant since went offline and I am not very fond of solutions in java,
so I recreated the whole thing as a [flask](https://flask.palletsprojects.com) app.

Enjoy!

## Setup

This is a flask application. You can run it like this (for development):

```shell
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ export SQLALCHEMY_DATABASE_URI="~/mytell.db"
$ export FLASK_APP=toldya
$ export FLASK_ENV=development
$ flask db migrate
$ flask db upgrade
$ flask run
```

This ends bringing up a development environment of this at port 5000 (the default Flask port).
There are a few environment variables that let you control how flask behaves and you can read more about them in the [upstream documentation](https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values).

For this particulat instance I've tried and give most of them reasonable values.
One of them is a bit brittle to say the least, since it holds the data for the
whole application and that one is the:

`SQLALCHEMY_DATABASE_URI`

This defines your backend database, so you want to have that defined to something that will actually
work, but you can use any database supported by the SQLAlchemy ORM. Detailed description on the url
format can be found again in the [upstream documentation](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)

### Run in production

For production I would recommend at least a different location for the database as `/tmp/tell.db`.
Ideally you'll set up a db at a remote RDBMS and expose it via the afforementioned `SQLALCHEMY_DATABASE_URI`.

Also as mentioned in the [upstream documentation]() you might not want to use the Flas webserver for production.
In this repo (and in `requirements.txt`) we provide an alternative with uwsgi and the shipped `uwsgi.ini`
to run this app in uwsgi exposed at port 8080 with `uwsgi --ini uwsgi.ini`.

You might also run this with a systemd-service, that could look something like this:

```ini
[Unit]
Description=uWSGI instance to serve toldya app
After=network.target

[Service]
User=naflask
Group=www-data
WorkingDirectory=/path/to/wherever/you/checked/this/out
ExecStart=/path/to/wherever/you/checked/this/out/venv/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target
```

### Run with Docker

I've included a `Dockerfile` in this repo that will plug together an alpine-based image
running uwsgi to serve this app. Keep in mind, that you might want to mount an
external volume to save the db file that you can set via `SQLALCHEMY_DATABASE_URI`.

If you go ahead and run `docker build -t toldya .` from the directory you've cloned
this repo to. The database is by default stored to `/data/toldya.db` in the container
and the `/data` directory is exposed as a volume, so you can mount it to your system
to generate persistance with the default sqlite3 database.

Remember that you can just as well set the above mentioned environment variable to
an external database as well.
