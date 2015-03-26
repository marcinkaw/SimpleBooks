"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import calendar
import datetime
from datetime import date

BOOKITEMDIRECTION = (
    ('out','KW'),
    ('in', 'KP')
)

class Book(models.Model):
	name = models.CharField(max_length=256)
	abbreviation = models.CharField(max_length=8)
	def __str__(self):
		return str(self.abbreviation)

class Currency(models.Model):
	name = models.CharField(max_length=50)
	abbreviation = models.CharField(max_length=4)
	def __str__(self):
		return str(self.abbreviation)

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

class Item(models.Model):
	report = models.ForeignKey(Report, related_name="Raport")
	itemDirection = models.CharField(max_length=3, choices=BOOKITEMDIRECTION)
	date = models.DateField('Date', default=date.today())
	number = models.IntegerField(default=0)
	month = models.IntegerField(default=int(datetime.date.today().month))
	year = models.IntegerField(default=int(datetime.date.today().year))
	abbreviation = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	party = models.CharField(max_length=200)
	def __str__(self):
		return self.abbreviation

