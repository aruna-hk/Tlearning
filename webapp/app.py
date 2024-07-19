#!/usr/bin/python3
from flask import Flask, g, request, abort, jsonify
from flask import session, redirect, make_response
from flask import url_for
from flask import render_template
from sqlalchemy import select, update, and_, or_, join, delete
from sqlalchemy.sql import func
import json
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from flask_socketio import SocketIO, emit
from models import Learner, Enroll, Unit, base, storage

app = Flask(__name__)
CORS(app)
storage.reload()

#enroll in unit
#get unit progress info all units~~specific units different API
#delete enrolled unit
@app.route('/learnplus/home/<user_id>/unit', methods=["GET", "POST", "DELETE"])
def unit(user_id):
    stmt = select(Learner.id).where(Learner.id == user_id)
    rp = storage.query(stmt)
    result = rp.first()
    if result is None:
        abort(404, "User Not found")
    if (request.method == "GET"):
        stmt = select(Unit.name, Enroll.pprogress).join(Enroll).where(Enroll.learnerId==user_id)
        rp = storage.query(stmt)
        result = rp.fetchall()
        if len(result) == 0:
            #no content
            return make_response("No content", 204)
        lis=[]
        for _entry in result:
            _entryd = {}
            _entryd['course_name'] = _entry[0]
            _entryd['progress'] = _entry[1]
            lis.append(_entryd)
        print(lis)
        return make_response(jsonify(lis), 200)

    if (request.method == "POST"):
        #enroll -- asume use send correct details
        info = request.get_json()
        info['learnerId'] = user_id
        new_unit = Enroll(**info)
        storage.new(new_unit)
        storage.save()
        return make_response(jsonify({201: "enrolled"}), 201);
    #otherwise -assume- user send correct registered unit
    units = request.get_json()
    print(units)
    for unit in units:
        stmt = delete(Enroll).where(Enroll.unitId == unit)
        storage.query(stmt)
    storage.save()
    return make_response("Done", 200)

#login page
@app.route("/learnplus/home/login", methods=["GET"], strict_slashes=False)
def login():
   stmt = select(Learner.password, Learner.imgURL, Learner.id)\
            .where(Learner.username == request.args.get('username'))
   _auth = storage.query(stmt).first()
   if _auth:
      if _auth[0] == request.args.get("password"):
          _user = {}
          _user['imgURL'] = _auth[1]
          _user['username'] = request.args.get("username")
          url = url_for('home', user_id=_auth[2])
          url = "http://localhost:8081" + url
          return redirect(url)
      else:
          abort(401, "unauthorized")
   return abort(404, "not found")


#create a/c
#return 201-created status code / (409 conflict if existing username)-integrity err
@app.route("/learnplus/home/learners", methods=["POST", "GET"])
def createac():
    if request.method == "GET":
        stmt = select(Learner)
        rp = storage.query(stmt)
        result = rp.fetchall() 
        return "learners enrolled"
    new_learner = Learner(**(request.get_json()))
    storage.new(new_learner)
    storage.save()
    login_url = url_for("login")+"?" + "username=<username>&password=<password>\n"
    
    return make_response("A/c created login with" + login_url, 201)

#return dictionary listings
def _entrys(results, typ=None):
    entries = []
    for entry in results:
        _entry = {}
        _entry['id'] = entry.id
        _entry['name'] = entry.name
        if typ is None:
            _entry['mentor'] = entry.mentor
        if typ is not None:
            _entry['pprogress'] = entry.pprogress
        entries.append(_entry)

    return entries


#return home screen
@app.route("/learnplus/home/<user_id>", strict_slashes=False)
def home(user_id=None):
    stmt = select(Enroll.unitId).where(Enroll.learnerId == user_id)
    uu = storage.query(stmt).fetchall()
    enrolled = []
    for value in uu:
        enrolled.append(storage.query(select(Unit.id, Unit.name, Unit.mentor).where(Unit.id == value[0])).first())
    enrolled = _entrys(enrolled, typ='tty')
    #user info for subsequent requests
    stmt2 = select(Learner.username, Learner.imgURL).where(Learner.id == user_id)
    rp = storage.query(stmt2)
    username, imgURL = rp.first()
    #units offered
    stmt = select(Unit.id, Unit.name, Unit.mentor)
    all_units = storage.query(stmt).fetchall()
    all_units = _entrys(all_units) 

    #schedule activities
    #none for now
    scheduled = []
    
    #create  home page
    return render_template("index.html", username=username, imgURL=imgURL, enrolled=enrolled, all=all_units, scheduled=scheduled)

#without user~~~landing
@app.route('/learnplus/home/', strict_slashes=False)
def home_2():
   return home()

   


#unitinfoupdate
#update unit progress
@app.route("/learnplus/home/<user_id>/<unit_id>/update", methods=["POST"])
def update(user_id, unit_id):
    return "updating progress info"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
