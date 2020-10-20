from db import db
from datetime import datetime

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mispar_osek = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<Provider {self.name} - {self.mispar_osek}>'


