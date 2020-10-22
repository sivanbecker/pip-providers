from datetime import datetime
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from models.provider import Provider
from db import db #pylint: disable=import-error
from schemas.provider import provider_schema, providers_schema

class ProviderResource(Resource):

    BASE_ROUTE = '/provider'
    API_ROUTE = '/provider/<string:mispar_osek>'
    def get(self, mispar_osek): #pylint: disable=no-self-use
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            return {'provider': provider_schema.dump(_provider)}
        except NoResultFound:
            return {'provider': None}, 404

    def post(self, mispar_osek): #pylint: disable=no-self-use
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
        except IntegrityError as exc:
            return {'message': str(exc)}


    def put(self, mispar_osek): #pylint: disable=no-self-use
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

    def delete(self, mispar_osek): #pylint: disable=no-self-use
        try:
            _provider = Provider.query.filter_by(mispar_osek=mispar_osek).one()
            db.session.delete(_provider)
            db.session.commit()
            return {'message': 'Provider Deleted'}
        except NoResultFound:
            return {'message': f'Provider with mispar-osek={mispar_osek} does not exist'}, 400

class ProviderListResource(Resource):

    BASE_ROUTE = '/providers'
    API_ROUTE = '/providers'
    def get(self): #pylint: disable=no-self-use
        return {'providers': providers_schema.dump(Provider.query.all())}
