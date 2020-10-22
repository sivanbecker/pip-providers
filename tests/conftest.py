import pytest
from datetime import datetime
from app import create_app
from db import db as _db
from flask import request
from models.provider import Provider
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database, drop_database
from sqlalchemy.orm.session import sessionmaker

class TestConfig:
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
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            session.commit()
            yield session
    except:
        session.rollback()
        raise
    finally:
        drop_database(engine.url)
        session.commit()
        session.close()


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
            
