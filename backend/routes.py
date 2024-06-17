from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data),200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    
    for dict in data:
        if   dict['id'] == id:
            return jsonify(dict),200
    return jsonify({"error" : "picture not found"}),404
    



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    id = request.form['id']
    pic_url = request.form['pic_url']
    event_country = request.form['event_country']
    event_state = request.form['event_state']
    event_city = request.form['event_city']
    event_date = request.form['event_date']
    

    for dict in data:
        if  dict['id'] == id:
            return jsonify({"Message": "picture with id {dict['id']} already present"}),302
            break
        else:
            data.append({'id':id, 
            'pic_url':pic_url,
            'event_country':event_country,
            'event_state': event_state,
            'event_city' : event_city,
            'event_date' : event_date
             })
            return jsonify({"message": "Picture created successfully"}), 201
    
   

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
