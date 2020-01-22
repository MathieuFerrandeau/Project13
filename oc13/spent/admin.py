from django.contrib import admin
from .models import Category, Outlay, UserOutlay

# Register your models here.

admin.site.register(Category)
admin.site.register(Outlay)
admin.site.register(UserOutlay)
