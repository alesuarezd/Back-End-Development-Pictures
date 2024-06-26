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
    
    for pic in data:
        if   pic['id'] == id:
            return jsonify(pic),200
    return jsonify({"error" : "picture not found"}),404
    



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    id = picture['id']
    pic_url = picture['pic_url']
    event_country = picture['event_country']
    event_state = picture['event_state']
    event_city = picture['event_city']
    event_date = picture['event_date']

    for pic in data:
        if pic['id'] == id:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}),302
    
    new_picture = {
        "id" : id,
        "pic_url" : pic_url,
        "event_country" : event_country,
        "event_state" : event_state,
        "event_city" : event_city,
        "event_date" : event_date
    }

    data.append(new_picture)

    return jsonify(new_picture),201


        
       
        
        
    
   

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    #getting data
    updated_picture = request.json
    #iterate data to check if the updated_picture already exists
    for index,picture in enumerate( data):
        if picture["id"] == id:
            data[index] = updated_picture
            return picture, 201
    return jsonify({"message": "picture not found"}),404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data.remove(data[index])
            return "", 204
    
    return jsonify({"message": "picture not found"}),404


   
