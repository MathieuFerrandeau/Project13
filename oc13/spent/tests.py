from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserOutlay, Outlay, Category
from .forms import RecordOutlayForm, UpdateOutlayForm
from .init_db import Fill_database

# Create your tests here.

class SpentViewTests(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user', password="password")
        category = Category.objects.create(name='test')
        outlay = Outlay.objects.create(name='test', category=category)
        useroutlay = UserOutlay.objects.create(user_name=user1, outlay=outlay, amount=200, payment_method='Virement',
                                      payment_date='2020-02-22')

    def test_outlay_recorded_view(self):
        """outlay_recorded"""
        response = self.client.get(reverse('spent:outlay_recorded'))
        self.assertEqual(response.status_code, 200)


class Fill_databaseTest(TestCase):

    def setup(self):  # pragma: no cover
        self.c = Fill_database()
        self.c.create_db()

    def test_create_categorie(self):
        logement = Category.objects.filter(name='Logement')
        self.assertIsNotNone(logement)

    def test_create_product(self):
        product = Outlay.objects.filter(category=2)
        self.assertIsNotNone(product)

class FormTestCase(TestCase):

    def test_record_outlay_form(self):
        form_data = {'amount': '2000',
                     'payment_method': 'Virement',
                     'payment_date': '2020-03-16'}

        form = RecordOutlayForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_outlay_form(self):
        form_data = form_data = {'amount': '3000',
                     'payment_method': 'Espèce',
                     'payment_date': '2020-07-23'}

        form = UpdateOutlayForm(data=form_data)
        self.assertTrue(form.is_valid())