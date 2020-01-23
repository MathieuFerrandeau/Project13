from django.test import TestCase
from .models import Category, Outlay, UserOutlay

class CategoryTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="nourriture")
        search = Category.objects.get(name="nourriture")
        self.assertEqual(category, search)

class OutlayTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="logement")
        self.outlay1 = Outlay(
                name="loyer",
                category=self.category,
                amount="700",
                payment_method="prélèvement",
                payment_date="2020-01-10",
                creation_date="2020-01-12")
        self.outlay1.save()

        self.outlay2 = Outlay(
            name="edf",
            category=self.category,
            amount="36.45",
            payment_method="virement",
            payment_date="2020-04-10",
            creation_date="2020-05-12")
        self.outlay2.save()

    def test_create_outlay(self):
        self.assertEqual(self.outlay1.category, self.category)
        self.assertEqual(self.outlay1.name, "loyer")
        self.assertEqual(self.outlay1.amount, "700")
        self.assertEqual(self.outlay1.payment_method, "prélèvement")
        self.assertEqual(self.outlay1.payment_date, "2020-01-10")
        self.assertNotEqual(self.outlay2.creation_date, "2020-01-12")
        self.assertEqual(self.outlay1.creation_date, "2020-01-12")
