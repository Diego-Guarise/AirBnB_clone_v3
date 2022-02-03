#!/usr/bin/python3
"""app_views index"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def return_status():
    status = {'status': 'OK'}
    return (jsonify(status))