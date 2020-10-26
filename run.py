from app import create_app # pylint: disable=import-error
from db import db # pylint: disable=import-error
from schemas.provider import ma

_app = create_app()
db.init_app(_app)
ma.init_app(_app)

@_app.before_first_request
def create_tables():
    db.create_all()
