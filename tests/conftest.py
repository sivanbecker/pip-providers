import os
from datetime import datetime
import pytest
import sqlalchemy as sa
from pytest_postgresql.factories import DatabaseJanitor
from psycopg2.errors import DuplicateDatabase

from app import create_app #pylint: disable=import-error
from db import db #pylint: disable=import-error
from models.provider import Provider

class TestConfig:
    ''' Just a generic test configuration '''
    TESTING = True
    WTF_CSRF_ENABLED = False
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
    except KeyError as exc:
        raise KeyError('TEST_DATABASE_URL not found. You must export a database ' +
                       'connection string to the environmental variable ' +
                       'TEST_DATABASE_URL in order to run tests.') from exc
    DB_OPTS = sa.engine.url.make_url(SQLALCHEMY_DATABASE_URI).translate_connect_args()
    try:
        POSTGRES_VER = os.environ['POSTGRES_VER']
    except KeyError as exc:
        raise KeyError('Missing POSTGRES_VER env variable.') from exc

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


@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_user = TestConfig.DB_OPTS.get("username")
    pg_host = TestConfig.DB_OPTS.get("host")
    pg_port = TestConfig.DB_OPTS.get("port")
    pg_db = TestConfig.DB_OPTS["database"]
    pg_pass = TestConfig.DB_OPTS.get("password")
    janitor = DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, TestConfig.POSTGRES_VER, pg_pass)
    try:
        janitor.init()
    except DuplicateDatabase:
        janitor.drop()
        janitor.init()

    @request.addfinalizer
    def drop_database(): #pylint: disable=unused-variable
        janitor.drop()


@pytest.fixture(scope='function')
def _app(database): #pylint: disable=unused-argument, redefined-outer-name
    current_app = create_app()
    current_app.config['SQLALCHEMY_DATABASE_URI'] = TestConfig.SQLALCHEMY_DATABASE_URI
    current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    return current_app

# @pytest.fixture(scope='session')
# def app(database):
#     '''
#     Create a Flask app context for the tests.
#     '''
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

#     return app


@pytest.fixture(scope='function')
def _db(_app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    # from db import db
    return db


@pytest.fixture
def client(_app, _db): #pylint: disable=redefined-outer-name, unused-argument
    # current_app = create_app()
    _app.config['TESTING'] = True
    # _app.config['SQLALCHEMY_DATABASE_URI'] = TestConfig.SQLALCHEMY_DATABASE_URI

    with _app.test_client() as clnt:
        with _app.app_context():
            _db.init_app(_app)
            _db.create_all()
            _db.session.add(TestConfig.TEST_PROVIDER1)
            _db.session.add(TestConfig.TEST_PROVIDER2)
            _db.session.commit()
            yield clnt
