#!/bin/bash
# simple script to run this app (Toldya)
# the virtual env needs to be activated!
flask db migrate
flask db upgrade
flask run --host=0.0.0.0
