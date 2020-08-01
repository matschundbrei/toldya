#!/usr/bin/env python3
import hashlib
from datetime import datetime
from flask import Flask
from flask import request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    ispub_dec = False
    if ispub == "on":
        ispub_dec = True
    newpost = Tell(id=gen_id, person=person, target=target, date=date, ispub=ispub_dec, text=text)
    db.session.add(newpost)
    db.session.commit()
    return gen_id

def getlatest():
    """
    get the latest (up to 5) public posts to display on the start page
    """
    return Tell.query.order_by(Tell.date).filter_by(ispub=True).limit(5)

def getpost(id):
    """
    get a specific post
    """
    return Tell.query.get(id)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        our_id = createpost(request.form['person'],
                            request.form['target'],
                            request.form['text'],
                            request.form['ispub'])
        return redirect("/{}".format(our_id))
    else:
        return render_template('index.html.j2', latest=getlatest())

@app.route('/<id>', methods=['GET'])
def showrecord(id=None):
    return render_template('show.html.j2',tell=getpost(id))
