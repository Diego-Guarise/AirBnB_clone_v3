#!/usr/bin/python3
"""All Place CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_places(city_id):
    """get all Place objects by city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        """displays all Places by City id"""
        all_places = storage.all(Place).values()
        city_places = []
        for place in all_places:
            if place.city_id == city_id:
                city_places.append(place.to_dict())
        return jsonify(city_places)
    else:
        """post a new Place object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        place_dict = request.get_json()
        if "user_id" not in place_dict:
            return jsonify("Missing user_id"), 400
        user = storage.get(User, place_dict["user_id"])
        if not user:
            abort(404)
        if "name" not in place_dict:
            return jsonify("Missing name"), 400
        try:
            new_place = Place(**place_dict)
            new_place.city_id = city_id
            new_place.user_id = place_dict["user_id"]
            new_place.save()
            return jsonify(new_place.to_dict()), 201
        except Exception as e:
            print(e)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def get_place(place_id):
    """get Place object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        """display Place object"""
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        """update Place object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        place_dict = request.get_json()
        if "name" in place_dict:
            place.name = place_dict["name"]
        if "description" in place_dict:
            place.description = place_dict["description"]
        if "number_rooms" in place_dict:
            place.number_rooms = place_dict["number_rooms"]
        if "number_bathrooms" in place_dict:
            place.number_bathrooms = place_dict["number_bathrooms"]
        if "max_guest" in place_dict:
            place.max_guest = place_dict["max_guest"]
        if "price_by_night" in place_dict:
            place.price_by_night = place_dict["price_by_night"]
        if "latitude" in place_dict:
            place.latitude = place_dict["latitude"]
        if "longitude" in place_dict:
            place.longitude = place_dict["longitude"]
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        """delete Place object"""
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
