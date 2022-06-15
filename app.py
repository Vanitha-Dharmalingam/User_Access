import json
import re

from bson import json_util
from bson.json_util import dumps
from flask import jsonify, request

from main import app, mongo

""" This API is used to add User to the User Table 
along with company and group id """


@app.route('/adduser', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _companyName = _json['companyName']
    _groupName = _json['groupName']
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    _company = get_companyID(_companyName)
    _companyID = None
    if not isinstance(_company, str):
        _companyID = _company['companyID']
    _group = get_groupID(_groupName)
    _groupID = None
    if not isinstance(_group, str):
        _groupID = _group['groupID']
    if (re.fullmatch(regex, _name)) and _companyID and _groupID and request.method == 'POST':
        id = mongo.db.user.insert_one({'username': _name, 'companyid': _companyID, 'groupid': _groupID})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return jsonify('Please Check whether the value given for username, company name and group name is valid.'
                       'User Name should be valid email address')


""" This API is used to view the list of users"""


@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


""" This API is used to add group"""


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


""" This method is used to get group with max group ID"""


def get_groupWithMaxID():
    groups = mongo.db.group.find().sort("groupID", -1)
    group = list(groups)[0]
    return json.loads(json_util.dumps(group))


""" This method returns the company id for the given company name"""


def get_companyID(companyName):
    company = mongo.db.company.find({"companyName": companyName})
    companylist = list(company)
    if len(companylist) > 0:
        output = companylist[0]
        return json.loads(json_util.dumps(output))
    else:
        return 'Not a valid company name'


""" This method returns the group id for the given group name"""


def get_groupID(groupName):
    group = mongo.db.group.find({"groupName": groupName})
    grouplist = list(group)
    if len(grouplist) > 0:
        output = grouplist[0]
        return json.loads(json_util.dumps(output))
    else:
        return 'Not a valid group name'


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
