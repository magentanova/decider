from flask import Blueprint, jsonify, request
from sqlalchemy.ext.serializer import loads, dumps

from Decider.db.db_setup import db_session
from Decider.db.models import Question, Token, TokenValue, User

api = Blueprint("api", __name__)

# CRUD tokens
@api.route("tokens")
def show_tokens():
    return jsonify({
        "tokens": Token.serialize_query_result(Token.query.filter({"active": 1}))
    })

@api.route("tokens", methods=["POST"])
def post_token():
    data = request.get_json()
    token = Token(name=data["name"], active=1 )
    db_session.add(token)
    db_session.commit()
    return jsonify({
        "saved_token": token.to_dict()
    })

@api.route("tokens", methods=["DELETE"])
def delete_token():
    return jsonify({
        "tokens": "are cool"
    })

# CRUD questions

# CRUD q-t associations

# CRUD token-value
