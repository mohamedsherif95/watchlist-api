from numpy import source
from .models import *
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    user_review=serializers.StringRelatedField(read_only=True)
    watchlist=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'

class Watchlistserializer(serializers.ModelSerializer):
    # review=ReviewSerializer(many=True,read_only=True )
    stream=serializers.CharField(source='stream.name')
    class Meta:
        model=Watchlist
        fields='__all__'
class StreamPlatFormSerializer(serializers.ModelSerializer):
   
    watchlist=Watchlistserializer(many=True,read_only=True)
    class Meta:
        model=StreamPlatFormn
        fields='__all__'

        
        
