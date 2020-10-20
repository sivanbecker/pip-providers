import os
from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, date
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from resources.provider import ProviderResource, ProviderListResource

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
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
    from schemas.provider import ma
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
