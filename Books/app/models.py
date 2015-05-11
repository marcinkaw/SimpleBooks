"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import calendar
import datetime
from datetime import date
from django.db.models import Q
from django.core.urlresolvers import reverse

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
								#help_text="Waluta raportu kasowego"
								)
	creator = models.ForeignKey(User, related_name="Utworzony przez",
								verbose_name="Utworzony przez")
	lastAmount = models.DecimalField('Przeniesienie', max_digits=10, decimal_places=2, default=0)
	trasnferAmount = models.DecimalField('Stan kasy poprzedni', max_digits=10, decimal_places=2, default=0)
	def __str__(self):
		return str(self.book.abbreviation + " " + self.currency.abbreviation)
	class Meta:
		get_latest_by = "fromDate"
	def get_absolute_url(self):
		return reverse('report_detail', args=[self.id])

class Item(models.Model):	
	BOOKITEMDIRECTION = (
		('out','KW'),
		('in', 'KP')
	)
	report = models.ForeignKey(Report, related_name="Raport")
	itemDirection = models.CharField(max_length=3, choices=BOOKITEMDIRECTION, default='out')
	itemDate = models.DateField('Date', default=date.today())
	title = models.CharField(max_length=200)
	party = models.CharField(max_length=200)
	creator = models.ForeignKey(User, related_name="Wpis utworzony przez",
								verbose_name="Wpis utworzony przez")
	amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

	def __str__(self):
		return self.abbreviation

	def get_absolute_url(self):
		return reverse('url', args=[self._check_id_field])

	def itemDirection_verbose(self):
		return dict(Item.BOOKITEMDIRECTION)[self.itemDirection]

	@property
	def number(self):
		items = Item.objects.filter(report = self.report).filter(itemDirection=self.itemDirection).filter(itemDate__lt=self.itemDate).order_by('itemDate').order_by('id')
		return str(self.itemDirection_verbose()) + "/" + str(len(items)+1).zfill(2) + "/" + str(self.itemDate.month).zfill(2) + "/" + str(self.report.book) + "/" + str(self.itemDate.year)

#class ItemsManaget(models.Manager):
#	def items_for_report(self, report)
#		return super(ItemsManager, self).get_queryset().filter(Q(report_id = report.id))
#