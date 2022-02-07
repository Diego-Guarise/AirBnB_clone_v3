#!/usr/bin/python3
"""All Place CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenitites(place_id):
    """Create a new view for the link between Place objects and Amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_of_all_amenity = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for value in place.amenities:
            list_of_all_amenity.append(value.to_dict())
    else:
        for value in place.amenity_ids:
            list_of_all_amenity.append(
                storage.get(Amenity, value).to_dict())
    return jsonify(list_of_all_amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def get_place_amenity(place_id, amenity_id):
    """get amenity by place id and amenity id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if place.id != amenity.place_id:
        abort(404)
    if request.method == 'DELETE':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.remove(amenity)
            place.save()
            return jsonify({})
        else:
            place.amenity_ids.remove(amenity_id)
            place.save()
        return jsonify({}), 200
    else:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                place.save()
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities_ids.append(amenity_id)
                place.save()
        return jsonify(amenity.to_dict()), 201
