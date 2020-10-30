import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.provider import ProviderResource, ProviderListResource #pylint: disable=import-error, no-name-in-module

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", os.environ.get('SQLALCHEMY_DATABASE_URI'))
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

def create_app():
    _app = Flask(__name__)
    CORS(_app)
    _app.config['DEBUG'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    api = Api(_app)

    api.add_resource(ProviderResource, ProviderResource.API_ROUTE)
    api.add_resource(ProviderListResource, ProviderListResource.API_ROUTE)

    @_app.route('/index')
    @_app.route('/')
    def index(): #pylint: disable=unused-variable
        return "Welcome to Service-Providers App"

    return _app

if __name__ == "__main__":
    app = create_app()
    from db import db
    from schemas.provider import ma
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
