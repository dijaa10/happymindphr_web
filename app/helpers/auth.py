from flask_jwt_extended import create_access_token
import datetime
import jwt
def encode_auth_token(self, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return create_access_token(user_id)
        # return jwt.encode(
        #     payload,
        #     app.config.get('SECRET_KEY'),
        #     algorithm='HS256'
        # )
    except Exception as e:
        return e


@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            auth_token, app.config.get("SECRET_KEY"), algorithms="HS256"
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return 1
    except jwt.InvalidTokenError:
        return 2
