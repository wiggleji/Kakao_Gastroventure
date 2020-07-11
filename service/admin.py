from django.contrib import admin

from service.models import Restaurant, Review, License
# Register your models here.

admin.register(Restaurant)
admin.register(Review)
admin.register(License)