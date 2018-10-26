=========
Mango-JWT
=========

Mango-JWT is a minimal JWT User Authentication tool for Django Rest Framework and MongoDB. Recommended for developers using django-rest-framework and pymongo. Not supported in versions below Django 2.0. ::

    pip install mango-jwt



Quick start
-----------

1. Add "mongo_auth" to your INSTALLED_APPS setting below "rest_framework"::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'mongo_auth',
    ]


2. Include the mongo_auth URLconf in your project urls.py like this::

    path('mongo_auth/', include('mongo_auth.urls')),

3. Add DB config in settings.py :- ::

    # Minimal settings (all mandatory)
    MANGO_JWT_SETTINGS = {
        "db_host": "some_db_host",
        "db_port": "some_db_port",
        "db_name": "for_example_auth_db",
        "db_user": "username",
        "db_pass": "password"
    }

    # Or use Advanced Settings (including optional settings)
    MANGO_JWT_SETTINGS = {
        "db_host": "some_db_host",
        "db_port": "some_db_port",
        "db_name": "for_example_auth_db",
        "db_user": "username",
        "db_pass": "password",
        "auth_collection": "name_your_auth_collection", # default is "user_profile"
        "fields": ("email", "password"), # default
        "jwt_secret": "secret", # default
        "jwt_life": 7 # default (in days)
    }

4. Make a POST request on http://127.0.0.1:8000/mongo_auth/signup/ with body as :- ::

    {
        "email": "some_email@email.com",
        "password": "some_password"
    }

5. Now login with these credentials at http://127.0.0.1:8000/mongo_auth/login/ :- ::

    {
        "email": "some_email@email.com",
        "password": "some_password"
    }

6. This will return a JWT. Pass this JWT in your request in "Authorization" header.

7. You can use **login_required** as a decorator in your views. Look at an example below.::

    from mongo_auth.utils import login_required


    @api_view(["GET"])
    @login_required
    def get_test(request):
        print(request.user)
        return Response(status=status.HTTP_200_OK,
                        data={"data": {"User already loggedin"}})


8. If user is already logged-in, you can use request.user to get user information (type dict).

Note: **login_required** cannot be used on class based views as decorators cannot be used over classes. I will be creating a Permission class or Mixin in the next release.

More Info
---------

1. Paaslib is used for password encryption with default scheme as "django_pbkdf2_sha256".

2. Only for Django 2.0 and above.

3. Dependent on "django-rest-framework" and "pymongo".

More Work To Do
---------------

1. Fields like "username", "mobile" or some unique field should be supportable for login.

2. Permission Class or Mixin to support Class based views.
