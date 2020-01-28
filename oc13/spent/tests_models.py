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
                category=self.category)
        self.outlay1.save()

        self.outlay2 = Outlay(
            name="edf",
            category=self.category)
        self.outlay2.save()

    def test_create_outlay(self):
        self.assertEqual(self.outlay1.category, self.category)

