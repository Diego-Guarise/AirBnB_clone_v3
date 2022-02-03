#!/usr/bin/python3
"""app_views index"""

from flask import jsonify
from api.v1.views import app_views
from holberton.AirBnB_clone_v3.models import amenity
from models import storage


@app_views.route('/status')
def return_status():
    status = {'status': 'OK'}
    return (jsonify(status))


@app_views.route('/api/v1/stats')
def return_status():
    """retrieves the number of each objects"""
    from AirBnB_clone_v3.models.amenity import Amenity
    from AirBnB_clone_v3.models.city import City
    from AirBnB_clone_v3.models.place import Place
    from AirBnB_clone_v3.models.review import Review
    from AirBnB_clone_v3.models.state import State
    from AirBnB_clone_v3.models.user import User


    dic = {}
    dic["amenity"] = storage.count(Amenity)
    dic["cities"] = storage.count(City)
    dic["places"] = storage.count(Place)
    dic["reviews"] = storage.count(Review)
    dic["states"] = storage.count(State)
    dic["users"] = storage.count(User)
    return dic
