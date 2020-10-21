from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ProviderSchema(ma.Schema):
    ''' Service Provider Marshmallow Schema'''
    class Meta:
        '''Marshmallow Schema Meta class'''
        fields = ("name", "mispar_osek", "service_type", "added")

provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)
