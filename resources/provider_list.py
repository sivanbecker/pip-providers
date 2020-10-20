from flask_restful import Resource
from models.provider import Provider
from schemas.provider import providers_schema
from app import api, app

class ProviderListResource(Resource):
    def get(self):
        return {'providers': providers_schema.dump(Provider.query.all())}

@app.before_first_request
def add_providers_resource():
    print("Adding resource ")
    api.add_resource(ProviderListResource, '/providers')
