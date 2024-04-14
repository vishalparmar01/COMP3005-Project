from django.test import TestCase

# Create your tests here.
from django.urls import reverse

class MyViewTestCase(TestCase):
    def test_my_view(self):
        # Simulate a GET request to the view
        response = self.client.get(reverse('register_member'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertContains(response, 'Expected content')

        # You can add more assertions as needed