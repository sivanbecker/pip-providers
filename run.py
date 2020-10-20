from app import app
from db import db
from schemas.provider import ma

db.init(app)
ma.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
