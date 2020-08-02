# Toldya

This is the recreation of an app that one of my former coworkers [Oli Zimpasser](https://github.com/oglimmer) made.
The source of the  [app called 'toldyouso' is still available here](https://github.com/oglimmer/toldyouso).

The formerly hosted variant since went offline and I am not very fond of solutions in java,
so I recreated the whole thing as a [flask](https://flask.palletsprojects.com) app.

Enjoy!

## Setup

This is a flask application. You can run it like this:

```shell
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ export SQLALCHEMY_DATABASE_URI="~/mytell.db"
$ export FLASK_APP=toldya.py
$ flask db migrate
$ flask db upgrade
$ flask run
```
There are a few environment variables that let you control how flask behaves and you can read more about them in the [upstream documentation](https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values).

For this particulat instance I've tried and give most of them reasonable values.
One of them is a bit brittle to say the least, since it holds the data for the
whole application and that one is the:

`SQLALCHEMY_DATABASE_URI`

This defines your backend database, so you want to have that defined to something that will actually
work, but you can use any database supported by the SQLAlchemy ORM. Detailed description on the url
format can be found again in the [upstream documentation](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)

### Run with Docker

TODO ;)
