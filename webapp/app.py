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
CORS(app, origins="*")
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
          url = "http://localhost:8080" + url
          print(url)
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
    return redirect("http://localhost:8080/learnplus/home/login")

#return dictionary listings
def _entrys(results):
    entries = []
    for entry in results:
        _entry = {}
        _entry['id'] = entry.id
        _entry['name'] = entry.name
        _entry['mentor'] = entry.mentor
        entries.append(_entry)

    return entries


#return home screen
@app.route("/learnplus/home/<user_id>", strict_slashes=False)
def home(user_id=None):

    #get enrolled unit ids and progres
    stmt = select(Enroll.unitId, Enroll.pprogress).where(Enroll.learnerId == user_id)
    Eunits = storage.query(stmt).fetchall()
    enrolled = []
    for value in Eunits:
        #id, name, mentor
        _dict = {}
        info = storage.query(select(Unit.name, Unit.mentor).where(Unit.id == value[0])).first()
        _dict['id'] = value[0]
        _dict['name'] = info[0]
        _dict['mentor'] = info[1]
        _dict['progress'] = value[1]
        enrolled.append(_dict)

    #Schedule activities
    stmt = select(Enroll.unitId, Enroll.S_time).where(Enroll.scheduled == 1)
    result = storage.query(stmt).fetchall()
    schedule = []
    for unit in result:
        _activity = {}
        res = storage.query(select(Unit.name).where(Unit.id == unit[0])).first()
        _activity['id'] = unit[0]
        _activity['Time'] = unit[1]
        _activity['name'] = res[0]
        schedule.append(_activity)

     

    #info to update user page before rendering
    stmt2 = select(Learner.username, Learner.imgURL).where(Learner.id == user_id)
    result = storage.query(stmt2).first()
    if user_id:
        username, imgURL = result
    else:
        username = None
        imgURL = None
    if imgURL is None:
        imgURL = "/images/user.png"

    #units offered -- all
    stmt = select(Unit.id, Unit.name, Unit.mentor)
    all_units = storage.query(stmt).fetchall()
    all_units = _entrys(all_units)
 

    #hist last visited
    res = storage.query(select(Enroll.unitId).where(Enroll.lastS == 1)).first()
    if res is None:
        lastStudied = None
    else:
        lastStudied = storage.query(select(Unit.name).where(Unit.id == res[0])).first()[0]


    #upcoming activity
    activity = {}
    if len(schedule) == 0:
        activity['name'] = None
        activity['Time'] = None
    else:
        activity = schedule[0]

    json = {"uid": user_id, "username":username, "imgURL":imgURL, "lastStudied":lastStudied, "enrolled":enrolled, \
            "all":all_units, "schedule":schedule, "scheduled":activity}
    if (request.headers.get("Accept") == "application/json"):
        return json
    return render_template("index.html",uid=user_id, username=username, imgURL=imgURL, lastStudied=lastStudied,\
                           enrolled=enrolled, all=all_units, schedule=schedule, scheduled=activity)

#without user~~~landing
@app.route('/learnplus/home/', strict_slashes=False)
def home_2():
    all_unit_stmt = select(Unit.id, Unit.name)
    results = storage.query(all_unit_stmt).fetchall()
    units_list = []
    for unit in results:
        _unit = {}
        _unit['id'] = unit.id
        _unit['name'] = unit.name
        units_list.append(_unit)

    return home()
    #return render_template("index.htm", all=units_list)

#update unit progress
#on get-- get next page/section progress update
#on post
@app.route("/learnplus/home/<user_id>/<unit_id>/update", methods=["GET", "POST"])
def update(user_id, unit_id):
    if request.method == "GET":
        stmt = select(Enroll.pprogress).where(and_(Enroll.learnerId == user_id, Enroll.unitId == unit_id))
        result = storage.query(stmt).first()
        print(result)
        update_stmt = update(Enroll.__tablename__).where(Enroll.unitId==unit_id).values(pprogress = 1)
        print(stmt)
        return "next topic"
    return "updating progress info"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
