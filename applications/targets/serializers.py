from django.contrib.gis.geos import Point
from rest_framework import serializers

from .models import Target, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    latitude = serializers.FloatField(required=True, source='location.x')
    longitude = serializers.FloatField(required=True, source='location.y')

    def create(self, validated_data):
        validated_data['location'] = Point(validated_data['location']['x'], validated_data['location']['y'])
        return super().create(validated_data)

    class Meta:
        model = Target
        fields = ('latitude', 'longitude','owner', 'radius', 'title', 'topic',)
