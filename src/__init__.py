from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, jsonify
from src.api.v1.models import db, serializer, search
from src.api.v1.routes.auth import auth
from src.api.v1.routes.videos import videos
from src.api.v1.routes.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger, swag_from
from src.config.swagger import swagger_config, template
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY'),
                            SQLALCHEMY_DATABASE_URI=os.environ.get(
                                'SQLALCHEMY_DATABASE_URI'),
                            SQLALCHEMY_TRACK_MODIFICATIONS=True,
                            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
                            JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
                            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
                            JWT_TOKEN_LOCATION=["headers", "query_string"],
                            JWT_QUERY_STRING_NAME="token",

                            MSEARCH_BACKEND='simple',
                            MSEARCH_PRIMARY_KEY='id',
                            MSEARCH_ENABLE=True,
                            SWAGGER={
        'title': "Techy Teacher Api",
        'uiversion': 3
    })
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": {
                "*",
            }
        }
    })

    db.app = app
    db.init_app(app)
    serializer.init_app(app)
    search.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(videos)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'not found'})

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_404(e):
        return jsonify({'error': 'something went wrong, we are working on it'})

    return app
