"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import calendar
import datetime
from datetime import date
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=256)
    abbreviation = models.CharField(max_length=8)
    def __str__(self):
        return str(self.abbreviation)

@python_2_unicode_compatible
class Currency(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    def __str__(self):
        return str(self.abbreviation)

@python_2_unicode_compatible
class Report(models.Model):
    fromDate = models.DateField('Data od', default=datetime.datetime(date.today().year, date.today().month, 1))
    toDate = models.DateField('Data do', default=datetime.datetime(date.today().year, date.today().month, calendar.monthrange(date.today().year, date.today().month)[1]))
    book = models.ForeignKey(Book, related_name="Kasa")
    currency = models.ForeignKey(Currency, related_name="Waluta",
                                verbose_name="Waluta raportu",
                                help_text="Waluta raportu kasowego")
    creator = models.ForeignKey(User, related_name="Utworzony przez",
                                verbose_name="Utworzony przez")
    lastAmount = models.DecimalField('Przeniesienie', max_digits=10, decimal_places=2, default=0)
    trasnferAmount = models.DecimalField('Stan kasy poprzedni', max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return str(self.book.abbreviation + " " + self.currency.abbreviation)

