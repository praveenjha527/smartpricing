from django.test import TestCase

# Create your tests here.


class APItest(TestCase):
    def api_test(self):
        url='http://localhost:8000/suggested_prices/'
        import  requests
        filter_params={
            ""
        }
        data=requests.get(url,filter_params)