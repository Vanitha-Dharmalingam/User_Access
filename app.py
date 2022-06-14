from bson import json_util

from main import app, mongo
from bson.json_util import dumps
from flask import jsonify, request
import pymongo
import json


@app.route('/adduser', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _companyName = _json['companyName']
    _groupName = _json['groupName']

    if _name and _companyName and _groupName and request.method == 'POST':

        id = mongo.db.user.insert_one({'username': _name, 'companyid': _companyName, 'groupid': _groupName})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/addgroup', methods=['POST'])
def add_group():
    _groupjson = request.json
    _groupname = _groupjson['groupname']
    _accessList = _groupjson['accesslist']
    if _groupname and request.method == 'POST':
        group = get_groupWithMaxID()
        _groupID = int(group['groupID']) + 1
        id = mongo.db.group.insert_one({'groupName': _groupname, 'groupID': _groupID})
        resp = jsonify('Group added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


def get_groupWithMaxID():
    groups = mongo.db.group.find().sort([("groupID", pymongo.DESCENDING)]).limit(1)
    group = list(groups)[0]
    return json.loads(json_util.dumps(group))


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()
