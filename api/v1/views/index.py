#!/usr/bin/python3
"""app_views index"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def return_status():
    """return status"""
    status = {'status': 'OK'}
    return (jsonify(status))


@app_views.route('/stats')
def return_stats():
    """retrieves number of each class object"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    stats = {}
    stats["amenities"] = storage.count(Amenity)
    stats["cities"] = storage.count(City)
    stats["places"] = storage.count(Place)
    stats["reviews"] = storage.count(Review)
    stats["states"] = storage.count(State)
    stats["users"] = storage.count(User)
    return (jsonify(stats))
