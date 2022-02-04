#!/usr/bin/python3
"""All City CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities(state_id):
    """get list of cities by state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        all_cities = storage.all(City).values()
        state_cities = []
        for city in all_cities:
            if city.state_id == state_id:
                state_cities.append(city.to_dict())
        return jsonify(state_cities)
    else:
        """post a new City object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        city_dict = request.get_json()
        if "name" not in city_dict:
            return jsonify("Missing name"), 400
        new_city = City(**city_dict)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_city(city_id):
    """get City object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'PUT':
        """updates City object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        city_dict = request.get_json()
        try:
            city.name = city_dict["name"]
            storage.save()
        except Exception:
            pass
        return jsonify(city.to_dict()), 200
    else:
        """deletes City object"""
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
