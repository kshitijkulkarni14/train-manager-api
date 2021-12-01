from django.http import response
from django.test import SimpleTestCase, Client
from django.urls.base import reverse
from trainDepartureViewer.api.v1 import views
from trainDepartureViewer.api.v1 import constants
from trainDepartureViewer.autz import credentials
# Create your tests here.


class TestViews(SimpleTestCase):

    def test_get_stations(self):
        client = Client()
        response = client.get(reverse('stations'))
        self.assertEqual(response.status_code, 401)

    def test_get_trains(self):
        client = Client()
        response = client.get(reverse('trains'))
        self.assertEqual(response.status_code, 401)

    def test_get_api_token(self):
        client = Client()
        response = client.post(reverse('api_token'), {constants.USERNAME: credentials.USERNAME, constants.PASSWORD: credentials.PASSWORD })
        self.assertEqual(response.status_code, 200)

    def test_get_train_category(self):
        result = views.get_train_category(constants.IC)
        self.assertEqual(constants.INTER_CITY, result)
