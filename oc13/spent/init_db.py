"""Fill the Database"""
import json
from django.db.utils import DataError, IntegrityError
from .models import Category, Outlay


class Fill_database():
    """Initializes the database"""

    def create_db(self):
        with open('spent/json/init_db.json') as json_data:
            data = json.load(json_data)
            data_length = len(data["categories"]) - 1
        i = 0
        while i <= data_length:
            for category in data["categories"][i]:
                new_category = Category.objects.create(name=category)
                for outlays in data["categories"][i][category]:
                    name = outlays
                    try:
                        Outlay.objects.create(name=name, category=new_category)

                    except KeyError:
                        pass

                    except DataError:
                        pass

                    except IntegrityError:
                        pass
            i = i + 1
