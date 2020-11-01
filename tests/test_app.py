from resources.provider import provider_schema, ProviderListResource, ProviderResource


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Welcome to Service-Providers App' in resp.response


def test_get_provider(client, _provider1_in_db):
    resp = client.get(
        f"{ProviderResource.BASE_ROUTE}/{_provider1_in_db.mispar_osek}")
    assert provider_schema.dump(_provider1_in_db) == resp.json['provider']


def test_get_non_existing_provider(client, _provider1_obj):
    resp = client.get(
        f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}")
    assert resp.is_json
    assert resp.json['provider'] is None


def test_get_providers(client, _providers_in_db):
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
    assert provider_schema.dump(_providers_in_db[0]) in resp.json['providers']
    assert provider_schema.dump(_providers_in_db[1]) in resp.json['providers']


def test_create_new_provider(client, _provider1_obj):

    resp = client.post(f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}",
                       json=dict(service_type=_provider1_obj.service_type,
                                 name=_provider1_obj.name))
    assert resp.is_json
    assert str(
        _provider1_obj.mispar_osek) == resp.json['provider']['mispar_osek']


def test_create_new_provider_with_duplicate_mispar_osek(client, _provider1_obj):
    resp = client.post(f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}",
                       json=dict(service_type=_provider1_obj.service_type,
                                 name=_provider1_obj.name))
    assert resp.status_code == 200
    resp2 = client.post(f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}",
                        json=dict(service_type=_provider1_obj.service_type,
                                  name=_provider1_obj.name))
    assert resp2.status_code == 400
    assert resp.is_json
    assert resp2.json == {'message':
                          f'Provider with mispar-osek={_provider1_obj.mispar_osek} already exists'}


def test_delete_provider(client, _provider1_in_db):
    resp_delete = client.delete(
        f"{ProviderResource.BASE_ROUTE}/{_provider1_in_db.mispar_osek}")
    assert resp_delete.is_json
    assert resp_delete.json == {'message': 'Provider Deleted'}


def test_delete_non_existing_provider(client, _provider1_obj):
    resp_delete = client.delete(
        f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}")
    assert resp_delete.status_code == 400
    assert resp_delete.is_json
    assert resp_delete.json == {'message':
                                f'Provider with mispar-osek={_provider1_obj.mispar_osek} does not exist'}  # pylint: disable=line-too-long


def test_update_existing_provider(client, _provider1_in_db):
    new_name = _provider1_in_db.name + '_new'
    new_service_type = _provider1_in_db.service_type + '_new'
    resp_update = client.put(f"{ProviderResource.BASE_ROUTE}/{_provider1_in_db.mispar_osek}",
                             json=dict(service_type=new_service_type,
                                       name=new_name))
    assert resp_update.is_json
    assert resp_update.json == {'message': 'Provider updated'}
    resp_after_db_update = client.get(
        f"{ProviderResource.BASE_ROUTE}/{_provider1_in_db.mispar_osek}")
    assert _provider1_in_db.name == resp_after_db_update.json['provider']['name']


def test_update_non_existing_provider(client, _provider1_obj):
    _provider1_obj.name += '_new'
    _provider1_obj.service_type += '_new'
    resp_update = client.put(f"{ProviderResource.BASE_ROUTE}/{_provider1_obj.mispar_osek}",
                             json=dict(service_type=_provider1_obj.service_type,
                                       name=_provider1_obj.name))
    assert resp_update.is_json
    assert resp_update.status_code == 201
    assert resp_update.json['provider']['mispar_osek'] == str(
        _provider1_obj.mispar_osek)
    assert resp_update.json['provider']['name'] == _provider1_obj.name
    assert resp_update.json['provider']['service_type'] == _provider1_obj.service_type

def test_heroku_app(heroku_client):
    resp = heroku_client.get('/')
    assert resp.status_code == 200
    assert resp.data == b'Welcome to Service-Providers App'
