#!/usr/bin/python3
"""All State CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """get a list of all State objects"""
    if request.method == 'GET':
        states = storage.all(State).values()
        states_dict = []
        for state in states:
            state_dict = state.to_dict()
            states_dict.append(state_dict)
        return (jsonify(states_dict))
    else:
        """creates new State object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        state_dict = request.get_json()
        if "name" not in state_dict:
            return (jsonify("Missing name"), 400)
        new_state = State(**state_dict)
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_state(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        """display state as JSON"""
        state = state.to_dict()
        return (jsonify(state))
    elif request.method == 'PUT':
        """edit state by id"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        state_dict = request.get_json()
        try:
            state.name = state_dict["name"]
            storage.save()
        except Exception:
            pass
        return (jsonify(state.to_dict()), 200)
    else:
        """delete state by id"""
        storage.delete(state)
        storage.save()
        return (jsonify({})), 200
