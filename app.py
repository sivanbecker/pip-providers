import os
from flask import Flask
from flask_restful import Api

from resources.provider import ProviderResource, ProviderListResource #pylint: disable=import-error, no-name-in-module

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", os.environ.get('SQLALCHEMY_DATABASE_URI'))
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
api = Api(app)

api.add_resource(ProviderResource, '/provider/<string:mispar_osek>')
api.add_resource(ProviderListResource, '/providers')

if __name__ == "__main__":
    from db import db
    from schemas.provider import ma #pylint: disable=import-error
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
