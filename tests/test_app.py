from flask import url_for
from resources.provider import ProviderListResource

def test_app(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Welcome to Service-Providers App' in resp.response
