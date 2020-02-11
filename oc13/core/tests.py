"""Test core views"""
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class CoreViewsTests(TestCase):
    """Test core views"""
    def test_index_returns_200(self):
        """Test index views"""
        response = self.client.get(reverse('core:index'))
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(' <hr class="divider my-4">', html)

    def test_credits_returns_200(self):
        """Test credits views"""
        response = self.client.get(reverse('core:credits'))
        self.assertEqual(response.status_code, 200)
