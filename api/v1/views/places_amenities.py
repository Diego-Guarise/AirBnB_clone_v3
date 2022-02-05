#!/usr/bin/python3
"""All Place CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenitites(place_id=None):
    """Create a new view for the link between Place objects and Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        if STORAGE_TYPE == 'db':
            place_amenities = place.amenities
        else:
            place_amen_ids = place.amenities
            place_amenities = []
            for amen in place_amen_ids:
                response.append(storage.get(Amenity, amen))
        place_amenities = [
            obj.to_json() for obj in place_amenities
            ]
            """
            for amenity in amenities:
                if amenity.place_id == place_id:
                    place_amenities.append(amenity.to_dict())
                    """
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def get_amenity(place_id=None, amenity_id=None):
    """get amenity by place id and amenity id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        if place.id != amenity.place_id:
            abort(404)
        if STORAGE_TYPE == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        place.save()
        return jsonify({}), 200
    else:
        if place.id == amenity.place_id:
            return jsonify(amenity.to_dict()), 200
        if STORAGE_TYPE == 'db':
            place.amenities.append(amenity)
        else:
            place.amenities = amenity
        return jsonify(amenity.to_json()), 201
