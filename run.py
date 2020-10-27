from app import create_app # pylint: disable=import-error
from db import db # pylint: disable=import-error
from schemas.provider import ma


def run(production=True):

    _app = create_app()

    if production:
        db.init_app(_app)
        ma.init_app(_app)

        @_app.before_first_request
        def create_tables(): #pylint: disable=unused-variable
            db.create_all()

    return _app

_app = run()
