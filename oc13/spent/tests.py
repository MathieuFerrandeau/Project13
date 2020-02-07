from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserOutlay, Outlay, Category
from .forms import RecordOutlayForm, UpdateOutlayForm
from .init_db import Fill_database

# Create your tests here.

class SpentViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'user'
        self.email = 'test@test.com'
        self.password = 'password'
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        self.category = Category.objects.create(name='test')
        self.outlay = Outlay.objects.create(name='test', category=self.category)
        self.useroutlay = UserOutlay.objects.create(user_name=self.user, outlay=self.outlay, amount=200, payment_method='Virement',
                                      payment_date='2020-02-22')

    def test_outlay_recorded_view(self):
        """outlay_recorded"""
        response = self.client.get(reverse('spent:outlay_recorded'))
        self.assertEqual(response.status_code, 200)

    def test_record_outlay_view(self):
        response = self.client.get(reverse('spent:record_outlay'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('spent:record_outlay'))
        self.assertEqual(response.status_code, 200)
        print(self.outlay)
        response = self.client.post('/record-outlay/', {'categories': self.category,
                                                        'outlay': self.outlay})
        self.assertEqual(response.status_code, 200)

    def test_outlay_modification_view(self):
        response = self.client.get('/outlay-modification/3/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get('/outlay-modification/4/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/outlay-modification/4/',
                                    {'amount': '300',
                                     'payment_method': 'Virement',
                                     'payment_date': '2020-04-16'})
        self.assertEqual(response.status_code, 200)

    def test_deleted_outlay_view(self):
        response = self.client.get('/outlay-deleted/3/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get('/outlay-deleted/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/outlay-deleted/1/', {'bouton_selected': '1'})
        self.assertEqual(response.status_code, 200)

    def test_history_view(self):
        """History"""
        response = self.client.get(reverse('spent:history'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('spent:history'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('spent:history'), {'month_list': '1',
                                                              'user_outlaymonth': '1',
                                                              'mois': '1',
                                                              'date': '2020',
                                                              'amount': "000"})
        self.assertEqual(response.status_code, 200)

    def test_empty_useroutlay_view(self):
        response = self.client.get(reverse('spent:empty_useroutlay'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('spent:empty_useroutlay'))
        self.assertEqual(response.status_code, 200)


class FillDatabaseTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Logement")
        outlay = Outlay.objects.create(name="Loyer", category=category)

    def test_create_categorie(self):
        logement = Category.objects.get(name='Logement')
        self.assertEqual(logement.name, 'Logement')

    def test_create_product(self):
        product = Outlay.objects.get(category=2)
        self.assertEqual(product.name, 'Loyer')


class FormTestCase(TestCase):

    def test_record_outlay_form(self):
        form_data = {'amount': '2000',
                     'payment_method': 'Virement',
                     'payment_date': '2020-03-16'}

        form = RecordOutlayForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_outlay_form(self):
        form_data = {'amount': '3000',
                     'payment_method': 'Espèce',
                     'payment_date': '2020-07-23'}

        form = UpdateOutlayForm(data=form_data)
        self.assertTrue(form.is_valid())
