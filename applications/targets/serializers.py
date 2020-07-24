from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Target, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):
    MAX_COUNT_TARGETS_PER_USER = 10

    owner = serializers.ReadOnlyField(source='owner.id')
    latitude = serializers.FloatField(required=True, source='location.x')
    longitude = serializers.FloatField(required=True, source='location.y')

    def create(self, validated_data):
        validated_data['location'] = Point(validated_data['location']['x'], validated_data['location']['y'])
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        if user.target_set.count() >= self.MAX_COUNT_TARGETS_PER_USER:
            raise serializers.ValidationError(_('Maximum number of targets exceeded'))

        return super().validate(data)

    class Meta:
        model = Target
        fields = ('id', 'latitude', 'longitude', 'owner', 'radius', 'title', 'topic', )
