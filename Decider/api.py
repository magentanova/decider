import random
from flask import Blueprint, jsonify, request

from Decider.db.db_setup import db_session
from Decider.db.models import Question, QuestionEffect, Token, TokenValue, User

api = Blueprint("api", __name__)

# CRUD (just create, and not even then) portraits
@api.route("portraits", methods=["POST"])
def save_portrait(): 
    portrait_data = request.get_json()["data"]
    # here is where we would
        # save to S3 
        # save an item linked to the user, etc., at that S3 URL
    return jsonify({
        "message": "Got a cool shaded portrait. Thanks!"
    })

# CRUD questions
@api.route("questions")
def read_questions():
    return jsonify({
        "questions": Question.serialize_query_result(Question.query.filter(Question.active == True))
    })

@api.route("questions/random")
def get_random_question():
    return jsonify(random.choice(Question.serialize_query_result(Question.query.filter(Question.active == True))))

@api.route("questions", methods=["POST"])
def create_question():
    data = request.get_json()
    question = Question(name=data["name"], active=1 )
    db_session.add(question)
    db_session.commit()
    return jsonify({
        "saved_question": question.to_dict()
    })

@api.route("questions", methods=["DELETE"])
def delete_question():
    return jsonify({
        "questions": "got deleted"
    })

# CRUD tokens
@api.route("tokens")
def read_tokens():
    return jsonify({
        "tokens": Token.serialize_query_result(Token.query.filter(Token.active == 1))
    })

@api.route("tokens", methods=["POST"])
def create_token():
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
        "tokens": "got deleted"
    })


# CRUD token-values
@api.route("token_values")
def read_token_values():
    user_id = request.args.get("user_id")
    if not user_id:
        return "you must provide a `user_id` query parameter", 400
    return jsonify(TokenValue.serialize_query_result(TokenValue.query.filter(TokenValue.user_id == user_id)))

@api.route("token_values", methods=["POST"])
def create_or_update_token_value():
    request_data = request.get_json()
    print(request_data)

    # interpret answer as sign for the token delta
    sign = 1 if request_data['answer'] == 'yes' else -1

    # find the tokens affected by this question
    question_effects = QuestionEffect.query.filter(QuestionEffect.question_id == request_data["question_id"])
    
    # get all the token values corresponding to this user (excess results, but fewer queries)
        # organize into a lookup table by token id
    token_values = TokenValue.query.filter(TokenValue.user_id == request_data["user_id"])
    token_values_by_token_id = {}
    for val in token_values: 
        token_values_by_token_id[val.token_id] = val 

    # for every relevant token...
    updated_tokens = []
    for effect in question_effects:
        token = effect.token 
        # see if this user has such a token value
        token_value = token_values_by_token_id.get(token.id)
        if not token_value: 
            # otherwise make a new one
            token_value = TokenValue(
                user_id=request_data["user_id"],
                token_id=token.id,
                value=0
            )
        # now add to session, mark as dirty
        db_session.add(token_value)
        token_value.value = max(min(token_value.value + effect.delta * sign, 100),0)
        updated_tokens.append(token_value)

    # make all updates
    db_session.commit()
    return jsonify(TokenValue.serialize_query_result(updated_tokens))
    
@api.route("token_values/reset", methods=["POST"])
def reset_token_values():
    user_id = request.args.get("user_id")
    if not user_id:
        return "you must provide a `user_id` query parameter", 400
    # delete all existing token values for this user
    TokenValue.query.filter(TokenValue.user_id == user_id).delete()
    
    # get all tokens
    all_tokens = Token.query.filter(Token.active == True)

    # and create a new token value for the user for that token
    new_token_values = []
    for token in all_tokens:
        token_value = TokenValue(token_id=token.id, user_id=user_id, value=50)
        token_value.token = token
        db_session.add(token_value)
        new_token_values.append(token_value)

    db_session.commit()
    print(new_token_values)
    return jsonify(TokenValue.serialize_query_result(new_token_values))

@api.route("token_values", methods=["DELETE"])
def delete_token_values():
    return jsonify({
        "token_values": "got deleted"
    })
