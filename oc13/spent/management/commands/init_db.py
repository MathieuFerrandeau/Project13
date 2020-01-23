from django.core.management.base import BaseCommand
from spent.init_db import Fill_database
from spent.models import Category


class Command(BaseCommand):
    """Initializes the database"""
    help = 'Initializes the database'

    ALL_ENTRIES_LIST = Category.objects.exists()

    def handle(self, *args, **options):
        if self.ALL_ENTRIES_LIST is False:
            db = Fill_database()
            db.create_db()
            self.stdout.write('La base de données a bien été initialisée.')
        else:
            self.stdout.write('La base de données existe déja.')