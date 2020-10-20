from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ProviderSchema(ma.Schema):
    class Meta:
        fields = ("name", "mispar_osek", "service_type", "added")

provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)
