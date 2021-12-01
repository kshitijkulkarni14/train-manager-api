from django.test import SimpleTestCase
from django.urls import reverse, resolve
from trainDepartureViewer.api.v1 import urls
from trainDepartureViewer.api.v1 import views
# Create your tests here.

class TestViews(SimpleTestCase):
    def test_trains_url_is_resolved(self):
        url = reverse('trains')
        self.assertEqual(resolve(url).func, views.get_trains)

    def test_stations_url_is_resolved(self):
        url = reverse('stations')
        self.assertEqual(resolve(url).func, views.get_stations)

    def test_api_token_url_is_resolved(self):
        url = reverse('api_token')
        self.assertEqual(resolve(url).func, views.get_api_token)