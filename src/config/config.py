import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ["headers","query_string"]
JWT_QUERY_STRING_NAME = "token"
MSEARCH_BACKEND = 'simple'
MSEARCH_PRIMARY_KEY = 'id'
SQLALCHEMY_TRACK_MODIFICATIONS = True
MSEARCH_ENABLE = True
SWAGGER = {
    'title': "Techy Teachers Api",
    'uiversion': 3
}
