from rest_framework.test import APIRequestFactory, APITestCase
import json

factory = APIRequestFactory()
class Apitest(APITestCase):
     def test_get_data(self):
        """
        Ensure we can get the right format.
        """
        response = self.client.get('//')
        self.assertEqual(json.loads(response.content), {})