#!/usr/bin/env python3
import os
import hashlib
import json
import uuid
from datetime import datetime
from flask import Flask, request, redirect, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)

app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', default='sqlite:////tmp/tell.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)
captcha = FlaskSessionCaptcha(app)

class Tell(db.Model):
    """
    defining the db model
    """
    id = db.Column(db.String(64), unique=True, primary_key=True)
    person = db.Column(db.String(255), nullable=True, unique=False)
    target = db.Column(db.String(255), nullable=True, unique=False)
    date = db.Column(db.DateTime, nullable=False, unique=False)
    ispub = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=False, unique=False)

    def __repr__(self):
        return '<Tell %r>' % self.id

def createpost(person, target, text, ispub):
    """
    write a new post to db
    """
    date = datetime.utcnow()
    gen_id = hashlib.sha256("{}+{}+{}+{}".format(date.timestamp(), person, target, text).encode()).hexdigest()
    if ispub == "True":
        ispub=True
    else:
        ispub=False
    newpost = Tell(id=gen_id, person=person, target=target, date=date, ispub=ispub, text=text)
    db.session.add(newpost)
    db.session.commit()
    return gen_id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if captcha.validate():
            our_id = createpost(request.form['person'],
                                request.form['target'],
                                request.form['text'],
                                request.form['ispub'])
            return redirect("/{}".format(our_id))
        else:
            return render_template('error.html.j2', error="Captcha validation error!")
    else:
        latest=Tell.query.order_by(Tell.date).filter_by(ispub=True).limit(5)
        return render_template('index.html.j2', latest=latest)

@app.route('/<id>', methods=['GET'])
def showrecord(id=None):
    tell=Tell.query.get_or_404(id)
    return render_template('show.html.j2',tell=tell)

@app.route('/<id>/json', methods=['GET'])
def showrecord_json(id=None):
    tell=Tell.query.get_or_404(id)
    return json.dumps({
        'id': id,
        'person': tell.person,
        'target': tell.target,
        'date': tell.date.timestamp(),
        'text': tell.text }, indent=4)
