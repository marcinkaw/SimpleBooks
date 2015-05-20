"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
	"""Tests for the application views."""

	if django.VERSION[:2] >= (1, 7):
		# Django 1.7 requires an explicit setup() when running tests in PTVS
		@classmethod
		def setUpClass(cls):
			django.setup()
			user_inst = User.objects.create_user(username='test', email='testuser@test.com', password='top_secret')
			Book.objects.create(abbreviation='KAS', name='KAS')
			Currency.objects.create(abbreviation='PLN', name='PLN')
			book_inst = Book.objects.all().filter(abbreviation='KAS')[0]
			currency_inst = Currency.objects.all().filter(abbreviation='PLN')[0]
			Report.objects.create(book = book_inst, currency = currency_inst, creator = user_inst, lastAmount = 100, trasnferAmount = 200)

	def test_home(self):
		"""Tests the home page."""
		response = self.client.get('/')
		self.assertContains(response, 'Prosta kasa', 5, 200)

	def test_contact(self):
		"""Tests the contact page."""
		response = self.client.get('/contact')
		self.assertContains(response, 'Strona kontaktowa.', 1, 200)

	def test_about(self):
		"""Tests the about page."""
		response = self.client.get('/about')
		self.assertContains(response, 'Prosta webowa kasa', 1, 200)

	def test_report_detail302(self):
		"""Tests the report_detail page."""
		response = self.client.get('/report/detail/1/')
		self.assertContains(response, '', 1, 302)

	def test_report_detail(self):
		"""Tests the report_detail page."""
		self.client.login(username='test', password='top_secret')
		response = self.client.get('/report/detail/1/')
		self.assertContains(response, 'No items', 1, 200)
