from functools import wraps

import jwt
from flask import current_app, g, jsonify, make_response, request, session

from main.modules.auth.model import User


def verify_token():
    """
    This decorator function is used for verify token form cookies.
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            access_token_cookie = request.cookies.get("access_token")
            if not access_token_cookie:
                access_token_cookie = session.get("access_token")

            if not access_token_cookie:
                return make_response(jsonify({"message": "Access token not found"}), 401)

            try:
                access_token = jwt.decode(
                    access_token_cookie, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
                )
                jwt_identity = access_token["sub"]
                email = jwt_identity["email"]
                user = User.filter(email=email, only_first=True)
                g.user = user if user else None
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return make_response(jsonify({"message": "Access token has expired"}), 401)
            except jwt.InvalidTokenError:
                return make_response(jsonify({"message": "Invalid access token"}), 401)

        return decorated

    return decorator
