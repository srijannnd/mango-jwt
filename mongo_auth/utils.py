import uuid
import jwt
from passlib.context import CryptContext
from mongo_auth.db import jwt_secret, auth_collection
from mongo_auth.db import database
from rest_framework.response import Response
from rest_framework import status

pwd_context = CryptContext(
    default="django_pbkdf2_sha256",
    schemes=["django_argon2", "django_bcrypt", "django_bcrypt_sha256",
             "django_pbkdf2_sha256", "django_pbkdf2_sha1",
             "django_disabled"])


def create_unique_object_id():
    unique_object_id = "ID_{uuid}".format(uuid=uuid.uuid4())
    return unique_object_id


# Check if user if already logged in
def login_status(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    data = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    user_obj = None
    flag = False
    user_filter = database[auth_collection].find({"id": data["id"]}, {"_id": 0, "password": 0})
    if user_filter.count():
        flag = True
        user_obj = list(user_filter)[0]
    return flag, user_obj


# Should be used as a Decorator for Authorization in APIs
def login_required(f):
    def wrap(request):
        try:
            flag, user_obj = login_status(request)
            request.user = None
            if flag:
                request.user = user_obj
                return f(request)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"data": "Not logged in"})
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"data": "Not logged in"})

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
