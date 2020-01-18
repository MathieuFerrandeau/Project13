from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.
class RegistrationViewTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='user', password="password")

    def test_login(self):
        response = self.client.post(reverse('registration:login'),
                                    {'username': 'user',
                                     'password': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('registration:register'),
                                    {'username': 'user',
                                     'email': 'testuser@email.com',
                                     'password1': 'password',
                                     'password2': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='user', password='password')
        self.client.logout()
        response = self.client.get(reverse('core:index'))
        self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])
        self.assertEqual(response.status_code, 200)

    def test_account(self):
        response = self.client.get(reverse('registration:account'))
        self.assertEqual(response.status_code, 302)
