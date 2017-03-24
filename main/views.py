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
import json
from django.http import HttpResponse
from wkhtmltopdf.views import PDFTemplateResponse
import math
import sys


def index(request):
    return HttpResponse("Hello, SimpleBooks!")


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if request.user.is_authenticated:
        all_reports = Report.objects.all().order_by('-fromDate')

        all_years = []
        for d in Report.objects.all().dates('fromDate', 'year').order_by('-fromDate'):
            if d.year not in all_years:
                all_years.append(d.year)

        all_books = Book.objects.all()

        context = {
            'all_reports': all_reports,
            'all_years': all_years,
            'all_books': all_books,
        }
        return render(
            request,
            'main/index.html',
            context
        )
    else:
        return redirect('login')


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    context = {'title': 'Kontakt',
                'message': 'Strona kontaktowa.',
                'year': datetime.datetime.now().year,
                }
    return render(
        request,
        'main/contact.html',
        context
        )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'main/about.html',
        context = {
            'title': 'O kasie',
            'message': 'Informacje o "Prostej kasie".',
            'year': datetime.datetime.now().year,
        })


@login_required
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
        items = Item.objects.all().filter(report=report).order_by('itemDate')
        context = {'report': report, 'form': form, 'items': items}
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")
    return render(
        request,
        'main/reportdetail.html',
        context
    )


@login_required
def report_print(request, pk, page_items=0):
    assert isinstance(request, HttpRequest)
    template = 'main/reportprint.html'
    page_items = int(page_items)
    if page_items <= 0:
        page_items = getattr(settings, 'PDF_NUMBER_OF_ITEMS_PER_PAGE', 20)
    elif page_items >= 25:
        page_items = 25

    company_info = getattr(settings, 'PDF_COMPANY_INFO', 'Brak')

    try:
        report = Report.objects.get(pk=pk)
        form = ReportForm(instance=report)
        items = Item.objects.all().filter(report=report).order_by('itemDate')
        if items.count() == 0:
            raise Http404("Brak wpisów!")
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")
    else:
        pages = int(math.ceil(items.count() / page_items))
        context = {
            'report': report,
            'form': form,
            'items': items,
            'page_range': range(pages),
            'items_per_page': page_items,
            'company_info': company_info,
        }
        cmd_options = {}

        pdf = PDFTemplateResponse(template=template, request=request, context=context, cmd_options=cmd_options)
        return HttpResponse(pdf.rendered_content, 'application/pdf')


@login_required
def receipt_print(request, pk):
    company_info = getattr(settings, 'PDF_COMPANY_INFO', 'Brak')

    try:
        report = Report.objects.get(pk=pk)
        items = Item.objects.all().filter(report=report).order_by('itemDate')
        if items.count() == 0:
            raise Http404("Brak wpisów")
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")
    else:
        context = {
            'items': items,
            'company_info': company_info,
        }
        cmd_options = {
            'orientation': 'landscape',
            'margin-top': 0,
            'margin-right': 0,
            'margin-left': 0,
            'margin-bottom': 0,
        }

        pdf = PDFTemplateResponse(template='main/reportprintreceipt.html', request=request, context=context, cmd_options=cmd_options)
        return HttpResponse(pdf.rendered_content, 'application/pdf')


@login_required
def receipt_print_single(request, pk):
    company_info = getattr(settings, 'PDF_COMPANY_INFO', 'Brak')

    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise Http404("Wpis nie istnieje!")
    else:
        lst = [item]
        context = {
            'items': lst,
            'company_info': company_info,
        }
        cmd_options = {
            'orientation': 'landscape',
            'margin-top': 0,
            'margin-right': 0,
            'margin-left': 0,
            'margin-bottom': 0,
        }

        pdf = PDFTemplateResponse(template='main/reportprintreceipt.html', request=request, context=context, cmd_options=cmd_options)
        return HttpResponse(pdf.rendered_content, 'application/pdf')


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
        context = {'form': form}
        return render(request, "main/reportnew.html", context)


@login_required
def report_edit(request, pk):
    try:
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")
    else:
        if request.method == 'POST':
            form = ReportForm(data=request.POST)
            if form.is_valid():
                report_form = ReportForm(data=request.POST, instance=report)
                report_form.save()
                return home(request)
        else:
            form = ReportForm(instance=report)
            context = {
                'form': form,
                'report': report,
            }
            return render(request, "main/reportedit.html", context)


@login_required
def item_add(request, rpk):
    # find report
    try:
        report = Report.objects.get(pk=rpk)
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")

    # if report found
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
    context = {'form': form, 'report': report}
    return render(request, "main/itemnew.html", context)


@login_required
def item_edit(request, rpk, pk):
    try:
        report = Report.objects.get(pk=rpk)
        item = Item.objects.get(pk=pk)
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")
    except Item.DoesNotExist:
        raise Http404("Wpis nie istnieje!")
    else:
        if request.method == 'POST':
            form = ItemForm(data=request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect(report)

        form = ItemForm(instance=item)
        context = {'form': form, 'report': report, 'item': item}
        return render(request, "main/itemedit.html", context)

@login_required
def item_delete(request, rpk, pk):
    assert isinstance(request, HttpRequest)
    try:
        Item.objects.get(pk=pk).delete()
    except Item.DoesNotExist:
        raise Http404("Wpis nie istnieje!")
    return report_detail(request, rpk)


def get_partys(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        items = Item.objects.filter(party__startswith=q).values('party').distinct()
        results = []
        for party in items:
            party_json = {}
            #party_json['id'] = party.id
            party_json['label'] = party['party']
            party_json['value'] = party['party']
            results.append(party_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_previous_report_amount(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            dt = request.POST.get('date', 'error')
            book = request.POST.get('book', 'error')
            proper_date = datetime.datetime.strptime(dt, '%d.%m.%Y')
            reports = Report.objects.filter(fromDate__month__lt=proper_date.month,
                                            fromDate__year__lte=proper_date.year,
                                            book__abbreviation=book).order_by('-fromDate')
            if reports.count() > 0:
                return HttpResponse(reports[0].amount)
        except ValueError:
            pass

    raise Http404()
