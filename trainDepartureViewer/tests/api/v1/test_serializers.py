from rest_framework.fields import DateField, DateTimeField
from trainDepartureViewer.api.v1.serializers import (
    TrainSerializer, TokenSerializer, StatusMessageSerializer, StationSerializer)
from django.test import SimpleTestCase

class TestSerializers(SimpleTestCase):
    status_message = {
        'status' : '200',
        'message' : 'OKAY'
    }

    train = {
        'plannedDateTime' : '2021-11-29T08:58:00+0100',
	    'direction' : 'Gouda Goverwelle',
	    'plannedTrack' : 2,
	    'trainCategory' : 'Intercity'
    }

    station = {
        'stationCode' : 'GVC',
	    'stationName' : 'Den Haag Centraal'
    }

    token = {
        'token' : 'abcdefgjhi'
    }

    status_message_serializer = StatusMessageSerializer
    train_serializer = TrainSerializer
    station_serializer = StationSerializer
    token_serializer = TokenSerializer
    

    def test_status_message_serializer(self):
        serialized_data = self.status_message_serializer(data=self.status_message)
        serialized_data.is_valid(raise_exception=True)
        self.assertEqual(serialized_data.data['status'], 200)
        self.assertEqual(serialized_data.data['message'], 'OKAY')

    def test_train_serializer(self):
        serialized_data = self.train_serializer(data=self.train)
        serialized_data.is_valid(raise_exception=True)
        self.assertEqual(serialized_data.data['plannedDateTime'], '2021-11-29T07:58:00Z')
        self.assertEqual(serialized_data.data['direction'], 'Gouda Goverwelle')
        self.assertEqual(serialized_data.data['plannedTrack'], 2)
        self.assertEqual(serialized_data.data['trainCategory'], 'Intercity')

    def test_station_serializer(self):
        serialized_data = self.station_serializer(data=self.station)
        serialized_data.is_valid(raise_exception=True)
        self.assertEqual(serialized_data.data['stationCode'], 'GVC')
        self.assertEqual(serialized_data.data['stationName'], 'Den Haag Centraal')

    def test_station_serializer(self):
        serialized_data = self.token_serializer(data=self.token)
        serialized_data.is_valid(raise_exception=True)
        self.assertEqual(serialized_data.data['token'], 'abcdefgjhi')
