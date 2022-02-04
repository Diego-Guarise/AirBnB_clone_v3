#!/usr/bin/python3
"""All Amenity CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def get_amenities():
    """get all amenities"""
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        amenities_dict = []
        for amenity in amenities:
            amenities_dict.append(amenity.to_dict())
        return jsonify(amenities_dict)
    else:
        """creates a new Amenity object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        amenity_dict = request.get_json()
        if "name" not in amenity_dict:
            return (jsonify("Missing name"), 400)
        new_amenity = Amenity(**amenity_dict)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        """display amenity object"""
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        """updates amenity object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        amenity_dict = request.get_json()
        try:
            amenity.name = amenity_dict["name"]
            storage.save()
        except Exception:
            pass
        return jsonify(amenity.to_dict()), 200
    else:
        """deletes an amenity object"""
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
