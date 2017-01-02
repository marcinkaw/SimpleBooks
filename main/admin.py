from django.contrib import admin
from .models import Currency, Book, Report, Item

# Register your models here.
admin.site.register(Currency)
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Item)
