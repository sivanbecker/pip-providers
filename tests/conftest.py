from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from app import create_app #pylint: disable=import-error
from db import db as _db #pylint: disable=import-error
from models.provider import Provider #pylint: disable=import-error

class TestConfig:
    ''' Just a generic test configuration '''
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@127.0.0.1:5432/test_service_providers'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TEST_PROVIDER1 = Provider(
        name='test_name1',
        mispar_osek=123,
        service_type='test_service_type',
        added=datetime.now()
        )
    TEST_PROVIDER2 = Provider(
        name='test_name2',
        mispar_osek=456,
        service_type='test_service_type',
        added=datetime.now()
        )

@pytest.fixture
def app():
    current_app = create_app()
    return current_app

@pytest.fixture(scope='session')
def gen_test_db():

    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(bind=engine)()
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            session.commit() #pylint: disable=no-member
            yield session
    except:
        session.rollback() #pylint: disable=no-member
        raise
    finally:
        drop_database(engine.url)
        session.commit() #pylint: disable=no-member
        session.close() #pylint: disable=no-member


@pytest.fixture
def client(gen_test_db):
    current_app = create_app()
    current_app.config['TESTING'] = True
    current_app.config['SQLALCHEMY_DATABASE_URI'] = TestConfig.SQLALCHEMY_DATABASE_URI

    with current_app.test_client() as clnt:
        with current_app.app_context():
            _db.init_app(current_app)
            _db.create_all()
            _db.session.add(TestConfig.TEST_PROVIDER1)
            _db.session.add(TestConfig.TEST_PROVIDER2)
            _db.session.commit()
            yield clnt
