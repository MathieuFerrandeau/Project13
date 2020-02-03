from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Outlay, UserOutlay

class CategoryTestCase(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Logement")
        search = Category.objects.get(name="Logement")
        self.assertEqual(category, search)

class OutlayTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="logement")
        self.outlay1 = Outlay(
                name="loyer",
                category=self.category)
        self.outlay1.save()

        self.outlay2 = Outlay(
            name="edf",
            category=self.category)
        self.outlay2.save()

    def test_outlay_exist(self):
        self.assertEqual(self.outlay1.category, self.category)

class UserOutlayTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='user', password="password")
        category = Category.objects.create(name="nourriture")
        outlay = Outlay.objects.create(name="Loyer", category=category)
        UserOutlay.objects.create(user_name=user,
                                  outlay=outlay,
                                  amount=200,
                                  payment_method='Espèce',
                                  payment_date='2020-07-16')

    def test_useroutlay_exist(self):
        useroutlay = UserOutlay.objects.get(amount=200)
        self.assertEqual(useroutlay.amount, 200)