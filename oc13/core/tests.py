from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class CoreViewsTests(TestCase):

    def test_index_returns_200(self):
        response = self.client.get(reverse('core:index'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(' <hr class="divider my-4">', html)

    def test_credits_returns_200(self):
        response = self.client.get(reverse('core:credits'))
        self.assertEqual(response.status_code, 200)