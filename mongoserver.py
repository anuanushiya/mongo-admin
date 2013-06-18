#!/usr/bin/env python
from bottle import route, run, static_file, redirect
from lib.template import render, render_str
from lib.mongo import MongoWrapper
import os
import json
from bson.objectid import ObjectId

def loader(d=dict()):
	d.update(dbs=MongoWrapper().getDbs())
	return d

@route('/static/<filename>')
def server_static(filename):
	root = os.path.dirname(__file__)
	root = os.path.abspath(os.path.join(root,"static"))
	return static_file(filename, root=root)


@route('/')
def index():
	return render("home.jade", loader(locals()))

@route('/monitor/<db_name>')
def api_show_collection(db_name=None):
	collections = MongoWrapper(db_name).getCollectionNames()
	return render("home.jade", loader(locals()))

@route('/monitor/<db_name>/<collection_name>')
def api_show_collection(db_name=None, collection_name=None):
	db = MongoWrapper(db_name).getCollection(collection_name)
	datas = []
	for d in db.find():
		if "_id" in d.keys():
			d["_id"] = str(d["_id"])
		d.update(json=json.dumps(d))
		datas.append(d)
	return render("list_data.jade", loader(locals()))

@route('/monitor/<db_name>/<collection_name>/<obj_id>/<action>')
def api_show_collection(db_name=None, collection_name=None, obj_id=None, action=None):
	db = MongoWrapper(db_name).getCollection(collection_name)
	obj = db.find_one({"_id": ObjectId(obj_id)})
	if obj:
		if action == "delete":
			db.remove(obj)
	redirect("/monitor/%s/%s" % (db_name,collection_name))

run(host='localhost', port=8080, reloader=True)