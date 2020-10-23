import json
from conftest import TestConfig
from resources.provider import provider_schema, ProviderListResource, ProviderResource

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Welcome to Service-Providers App' in resp.response

def test_get_provider(client, _provider1):
    resp = client.get(f"{ProviderResource.BASE_ROUTE}/{_provider1.mispar_osek}")
    assert provider_schema.dump(_provider1) == resp.json['provider']

def test_get_providers(client, _providers):
    '''
    at this stage we have a db called test_service_providers with
    two fake records.

    1. test get request of providers
    2. test response is a json
    3. test we get back from db the same record we inserted
    '''
    resp = client.get(ProviderListResource.BASE_ROUTE)
    assert resp.status_code == 200
    assert resp.is_json
    assert provider_schema.dump(_providers[0]) in resp.json['providers']
    assert provider_schema.dump(_providers[1]) in resp.json['providers']

def test_create_new_provider(client):

    resp = client.post(f"{ProviderResource.BASE_ROUTE}/{TestConfig.TEST_PROVIDER1.mispar_osek}",
                        json=dict(service_type=TestConfig.TEST_PROVIDER1.service_type,
                                name=TestConfig.TEST_PROVIDER1.name))
    assert resp.is_json
    assert TestConfig.TEST_PROVIDER1.mispar_osek == resp.json['provider']['mispar_osek']
