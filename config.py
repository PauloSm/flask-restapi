from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# This dictionary centralize database information used in this file and in the database.py
DATABASE_PARAMS = {
        'host': 'localhost',
        'database': 'books',
        'user': 'your username',
        'password': 'your password'
    }

class Config:
    """Class created with the purpose of centralizing the configuration of the application """
    DEBUG = True

    # Connection with the database
    DATABASE_URI = ('postgresql+psycopg2://' + DATABASE_PARAMS['user'] + ':' + DATABASE_PARAMS['password'] + '@' +
                    DATABASE_PARAMS['host'] + ':' + '5432/' + DATABASE_PARAMS['database'])
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration of api spec used for swagger
    API_DOC_CONFIGURATION = {
        'APISPEC_SPEC': APISpec(
            title='Book Project API',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    }
