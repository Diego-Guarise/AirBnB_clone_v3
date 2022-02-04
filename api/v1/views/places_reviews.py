#!/usr/bin/python3
"""All Review CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_reviews(place_id):
    """get all Review objects from place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        """displays all Reviews by place_id"""
        all_reviews = storage.all(Review).values()
        place_reviews = []
        for review in all_reviews:
            if review.place_id == place_id:
                place_reviews.append(review.to_dict())
        return jsonify(place_reviews)
    else:
        """creates a new Review object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        review_dict = request.get_json()
        if "user_id" not in review_dict:
            return jsonify("Missing user_id"), 400
        user = storage.get(User, review_dict["user_id"])
        if not user:
            abort(404)
        if "text" not in review_dict:
            return jsonify("Missing text"), 400
        new_review = Review(**review_dict)
        new_review.user_id = review_dict["user_id"]
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def get_review(review_id):
    """get Review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        """display one Review by id"""
        return jsonify(review.to_dict())
    elif request.method == 'PUT':
        """updates one Review by id"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        review_dict = request.get_json()
        try:
            review.text = review_dict["text"]
            storage.save()
        except Exception as e:
            print(e)
        return jsonify(review.to_dict()), 200
    else:
        """deletes Review object by id"""
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
