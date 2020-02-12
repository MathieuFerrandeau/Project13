"""Registration tests"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ConnexionForm, AccountUpdateForm, ContactForm


# Create your tests here.
class RegistrationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'user'
        self.email = 'test@test.com'
        self.password = 'password'
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('registration:login'),
                                    {'username': 'user',
                                     'password': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('registration:register'),
                                    {'username': 'user',
                                     'email': 'testuser@email.com',
                                     'password1': 'password',
                                     'password2': 'password'}, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='user', password='password')
        self.client.logout()
        self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])

    def test_account(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/account/', {'username': 'user',
                                                  'email': 'testuser@email.com'})
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.post(reverse('password_reset'),
                                    {'email': 'test@mail.fr'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_success_view(self):
        response = self.client.get(reverse('registration:success'))
        self.assertEqual(response.status_code, 200)

    def test_email_view(self):
        response = self.client.get('/contact-form/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('registration:success'),
                                    {'subject': 'sujet',
                                     'from_email': 'test@test.fr',
                                     'message': 'testtest'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_view(self):
        response = self.client.get('/password-reset/')
        self.assertEqual(response.status_code, 200)


class FormTestCase(TestCase):

    def test_connexion_form(self):
        form_data = {'username': 'user',
                     'password': 'password'}

        form = ConnexionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_account_update_form(self):
        form_data = {'username': 'useruser',
                     'email': 'test@test.fr'}

        form = AccountUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form(self):
        form_data = {'from_email': 'test@test.fr',
                     'message': 'test_message',
                     'subject': 'test_subject'}

        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
