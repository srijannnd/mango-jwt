from rest_framework.decorators import api_view
from mongo_auth.utils import create_unique_object_id, pwd_context
from mongo_auth.db import database, auth_collection, fields, jwt_life, jwt_secret
import jwt
import datetime
from mongo_auth import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


@api_view(["POST"])
def signup(request):
    try:
        data = request.data if request.data is not None else {}
        signup_data = {"id": create_unique_object_id()}
        for field in set(fields + ("email", "password")):
            if field in data:
                signup_data[field] = data[field]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error_msg": field.title() + " does not exist."})
        signup_data["password"] = pwd_context.hash(signup_data["password"])
        if database[auth_collection].find_one({"email": signup_data['email']}) is None:
            database[auth_collection].insert_one(signup_data)

            return Response(status=status.HTTP_200_OK,
                            data={"data": {
                                "email": signup_data['email']
                            }})
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                            data={"data": {"error_msg": messages.user_exists}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})


@api_view(["POST"])
def login(request):
    try:
        data = request.data if request.data is not None else {}
        email = data['email']
        password = data['password']
        user = database[auth_collection].find_one({"email": email}, {"_id": 0})
        if user is not None:
            if pwd_context.verify(password, user["password"]):
                token = jwt.encode({'id': user['id'],
                                    'exp': datetime.datetime.now() + datetime.timedelta(
                                        days=jwt_life)},
                                   jwt_secret, algorithm='HS256').decode('utf-8')
                return Response(status=status.HTTP_200_OK,
                                data={"data": {"token": token}})
            else:
                return Response(status=status.HTTP_200_OK,
                                data={"error_msg": messages.incorrect_password})
        else:
            return Response(status=status.HTTP_200_OK,
                            data={"data": {"error_msg": messages.user_not_found}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})
