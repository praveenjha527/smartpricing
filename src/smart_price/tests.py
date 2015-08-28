from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
import json

factory = APIRequestFactory()
class Apitest(APITestCase):
     def test_get_data(self):
        """
        Ensure we can get the right format.
        """
        response = self.client.get('//')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {})