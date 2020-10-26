from app import app # pylint: disable=import-error
from db import db # pylint: disable=import-error
from schemas.provider import ma

db.init_app(app)
ma.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
