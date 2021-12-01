from rest_framework import serializers

class TrainSerializer(serializers.Serializer):
	""" TrainSerializer serializer class.
        serailaizes Departure."""
	plannedDateTime = serializers.DateTimeField()
	direction = serializers.CharField()
	plannedTrack = serializers.IntegerField()
	trainCategory = serializers.CharField()

class StatusMessageSerializer(serializers.Serializer):
	""" StatusMessageSerializer serializer class.
		serailaizes StatusMessage."""
	status = serializers.IntegerField()
	message = serializers.CharField()

class TokenSerializer(serializers.Serializer):
	""" TokenSerializer serializer class
		serailaizes Token"""
	token = serializers.CharField()

class StationSerializer(serializers.Serializer):
	""" StationSerializer serializer class.
		serailaizes Station."""
	stationCode = serializers.CharField()
	stationName = serializers.CharField()
