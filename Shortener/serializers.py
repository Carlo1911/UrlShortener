from rest_framework import serializers
from Shortener.models import URLData

class URLDataSerializers(serializers.ModelSerializers):
    class meta:
        model = URLData
        field = '__all__'
