from flask import request
from datetime import datetime
from flask_restful import Resource
from models.provider import Provider
from db import db
from schemas.provider import provider_schema, providers_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class ProviderResource(Resource):

    def get(self, mispar_osek):
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            return {'provider': provider_schema.dump(_provider)}
        except NoResultFound:
            return {'provider': None}, 404

    def post(self, mispar_osek):
        if Provider.query.filter_by(mispar_osek=mispar_osek).count():
            return {'message': 'Provider with mispar-osek={mispar_osek} already exists'}, 400

        data = request.get_json()
        new_provider = Provider(
            name=data['name'],
            mispar_osek=mispar_osek,
            service_type=data['service_type'],
            added=datetime.now()
        )
        try:
            db.session.add(new_provider)
            db.session.commit()
            return {'provider': provider_schema.dump(new_provider)}
        except IntegrityError as e:
            return {'message': str(e)}


    def put(self, mispar_osek):
        data = request.get_json()
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            _provider.service_type = data['service_type']
            _provider.name = data['name']
            return {'message': 'Provider updated'}
        except NoResultFound:
            new_provider = Provider(
                name=data['name'],
                mispar_osek=mispar_osek,
                service_type=data['service_type'],
                added=datetime.now()
            )
            db.session.add(new_provider)
            db.session.commit()
            return {'provider': provider_schema.dump(new_provider)}, 201

    def delete(self, mispar_osek):
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            db.session.delete(_provider)
            db.session.commit()
            return {'message': 'Provider Deleted'}
        except NoResultFound:
            return {'message': f'Provider with mispar-osek={mispar_osek} does not exist'}, 400

class ProviderListResource(Resource):

    def get(self):
        return {'providers': providers_schema.dump(Provider.query.all())}
