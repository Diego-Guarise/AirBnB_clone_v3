#!/usr/bin/python3
"""All Place CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenitites(place_id):
    """Create a new view for the link between Place objects and Amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        place_amenities = []
        for amenity in amenities:
            if amenity.place_id == place_id:
                place_amenities.append(amenity.to_dict())
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def get_place_amenity(place_id, amenity_id):
    """get amenity by place id and amenity id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'DELETE':
        if place.id != amenity.place_id:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        if place.id == amenity.place_id:
            return jsonify(amenity.to_dict()), 200
        return Amenity(), 201