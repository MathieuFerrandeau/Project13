from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class CoreViewsTests(TestCase):

    def test_index_returns_200(self):
        response = self.client.get(reverse('core:index'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<h2 class="section-heading">INDEX</h2>', html)