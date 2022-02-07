#!/usr/bin/python3
"""All Place CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import environ


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenitites(place_id):
    """Create a new view for the link between Place objects and Amenity"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    list_of_all_amenity = []
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        for values in places.amenities:
            list_of_all_amenity.append(values.to_dict())
    else:
        for value in places.amenity_ids:
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
    if request.method == 'DELETE':
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            if place.id != amenity.place_id:
                abort(404)
            place.amenity.remove(amenity)
            place.save()
            return jsonify({})
        else:
            if place.id != amenity.place_id:
                abort(404)
            place.amenity_ids.remove(amenity_id)
            place.save()
        return jsonify({}), 200
    else:
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                place.save()
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities_ids.append(amenity)
                place.save()
        return jsonify(Amenity.to_dict()), 201
