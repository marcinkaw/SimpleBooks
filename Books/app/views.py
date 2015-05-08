"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	all_reports = Report.objects.all().order_by('-fromDate')
	context = {'all_reports' : all_reports}
	return render(
		request,
		'app/index.html',
		context_instance = RequestContext(request, context)
	)

def contact(request):
	"""Renders the contact page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/contact.html',
		context_instance = RequestContext(request,
		{
			'title':'Kontakt',
			'message':'Strona kontaktowa.',
			'year':datetime.now().year,
		})
	)

def about(request):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/about.html',
		context_instance = RequestContext(request,
		{
			'title':'O kasie',
			'message':'Informacje o "Prostej kasie".',
			'year':datetime.now().year,
		})
	)

def report_delete(request, pk):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	try:
		Report.objects.get(pk=pk).delete()
	except Report.DoesNotExist:
		raise Http404("Raport nie istnieje!")
	return redirect('home')

@login_required
def report_detail(request, pk):
	assert isinstance(request, HttpRequest)
	try:
		report = Report.objects.get(pk=pk)
		form = ReportForm(instance=report)
		items = Item.objects.all().filter(report=report)
		context = {'report' : report, 'form' : form, 'items' : items}
	except Report.DoesNotExist:
		raise Http404("Raport nie istnieje!")
	return render(
		request,
		'app/reportdetail.html',
		context_instance = RequestContext(request, context)
	)

@login_required
def report_add(request):
	if request.method == 'POST':
		report = Report(creator=request.user)
		form = ReportForm(data=request.POST, instance=report)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		# TODO Quick and dirty
		form_initials = {}
		if hasattr(settings, 'BOOKS_DEFAULT_BOOK'):
			form_initials['book'] = Book.objects.all().filter(abbreviation=settings.BOOKS_DEFAULT_BOOK)[0].id
		if hasattr(settings, 'BOOKS_DEFAULT_CURRENCY'):
			form_initials['currency'] = Currency.objects.all().filter(abbreviation=settings.BOOKS_DEFAULT_CURRENCY)[0].id
		form = ReportForm(initial=form_initials)
		context = {'form' : form}
	return render(request, "app/reportnew.html", context)

@login_required
def report_edit(request, pk):
	if request.method == 'POST':
		form = ReportForm(data=request.POST)
		if form.is_valid():
			try:
				report = Report.objects.get(pk=pk)
				report_form = ReportForm(data=request.POST, instance=report)
				report_form.save()
				context = {'report' : report, 'form' : report_form}
				return render(
					request,
					'app/reportdetail.html',
					context_instance = RequestContext(request, context)
				)
			except  Report.DoesNotExist:
				raise Http404("Raport nie istnieje!")
	
	return redirect('home')

@login_required
def item_add(request, rpk):
	# find report
	try:
		report = Report.objects.get(pk=rpk)
	except  Report.DoesNotExist:
		raise Http404("Raport nie istnieje!")
	
	# if report founf
	if request.method == 'POST':
		report = Report.objects.get(pk=rpk)
		item = Item(creator=request.user, report=report)
		form = ItemForm(data=request.POST, instance=item)
		if form.is_valid():
			form.save()
			#return report_detail(request, rpk)
			return redirect(report)
	else:
		form = ItemForm()
	context = {'form' : form, 'report' : report}
	return render(request, "app/itemnew.html", context)

def item_delete(request, rpk, pk):
	
	assert isinstance(request, HttpRequest)
	try:
		Item.objects.get(pk=pk).delete()
	except Report.DoesNotExist:
		raise Http404("Wpis nie istnieje!")
	return report_detail(request, rpk)