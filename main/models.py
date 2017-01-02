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
from django.db.models import Sum
from django.utils import timezone

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
	book = models.ForeignKey(Book, related_name="Kasa", verbose_name="Kasa")
	currency = models.ForeignKey(Currency, related_name="Waluta",
								verbose_name="Waluta raportu",
								#help_text="Waluta raportu kasowego"
								)
	creator = models.ForeignKey(User, related_name="Utworzony przez+",
								verbose_name="Utworzony przez")
	lastAmount = models.DecimalField('Przeniesienie', max_digits=10, decimal_places=2, default=0)
	trasnferAmount = models.DecimalField('Stan kasy poprzedni', max_digits=10, decimal_places=2, default=0)
	def __str__(self):
		return str(self.book.abbreviation + " " + self.currency.abbreviation)
	class Meta:
		get_latest_by = "fromDate"
	def get_absolute_url(self):
		return reverse('report_detail', args=[self.id])

	@property
	def sumIn(self):
		return Item.objects.filter(report = self).filter(itemDirection='in').aggregate(Sum('amount')).get('amount__sum',0)

	@property
	def sumOut(self):
		return Item.objects.filter(report = self).filter(itemDirection='out').aggregate(Sum('amount')).get('amount__sum',0)

	@property
	def amount(self):
		return float(self.lastAmount) + float(self.sumIn) - float(self.sumOut)


class Item(models.Model):	
	BOOKITEMDIRECTION = (
		('out','KW'),
		('in', 'KP')
	)
	report = models.ForeignKey(Report, related_name="Raport")
	itemDirection = models.CharField(max_length=3, choices=BOOKITEMDIRECTION, default='out')
	itemDate = models.DateField('Date', default=timezone.now)
	title = models.CharField(max_length=200)
	party = models.CharField(max_length=200)
	creator = models.ForeignKey(User, related_name="Wpis utworzony przez+",
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
		
		# manage items with the same date
		items_same_date = Item.objects.filter(report = self.report).filter(itemDirection=self.itemDirection).filter(itemDate=self.itemDate).order_by('id')
		ad = 1
		for it in items_same_date:
			if it.id==self.id:
				break
			ad = ad + 1

		return str(self.itemDirection_verbose()) + "/" + str(len(items)+ad).zfill(2) + "/" + str(self.itemDate.month).zfill(2) + "/" + str(self.report.book) + "/" + str(self.itemDate.year)

	@property
	def letter(self):
		items = Item.objects.filter(report = self.report).filter(itemDate__lt=self.itemDate).order_by('itemDate').order_by('id')
		
		# manage items with the same date
		items_same_date = Item.objects.filter(report = self.report).filter(itemDate=self.itemDate).order_by('id')
		ad = 1
		for it in items_same_date:
			if it.id==self.id:
				break
			ad = ad + 1

		return str(len(items)+ad)



#class ItemsManaget(models.Manager):
#	def items_for_report(self, report)
#		return super(ItemsManager, self).get_queryset().filter(Q(report_id = report.id))