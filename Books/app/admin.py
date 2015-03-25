from django.contrib import admin
from .models import Book, Currency, Report
# Register your models here.

admin.site.register(Book)
admin.site.register(Currency)
admin.site.register(Report)
