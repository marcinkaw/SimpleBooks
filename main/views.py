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


def index(request):
    return HttpResponse("Hello, SimpleBooks!")


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    all_reports = Report.objects.all().order_by('-fromDate')
    context = {'all_reports' : all_reports}
    return render(
        request,
        'main/index.html',
        context
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    context = { 'title':'Kontakt',
                'message':'Strona kontaktowa.',
                'year': datetime.datetime.now().year,}
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
        context = {'report' : report, 'form' : form, 'items' : items}
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

    try:
        report = Report.objects.get(pk=pk)
        form = ReportForm(instance=report)
        items = Item.objects.all().filter(report=report).order_by('itemDate')
        pages = int(math.ceil(items.count() / page_items))
        context = {
            'report': report,
            'form': form,
            'items': items,
            'page_range': range(pages),
            'items_per_page': page_items,
        }
    except Report.DoesNotExist:
        raise Http404("Raport nie istnieje!")

    cmd_options = {}

    pdf = PDFTemplateResponse(template=template, request=request, context=context, cmd_options=cmd_options)

    return HttpResponse(pdf.rendered_content, 'application/pdf')


@login_required
def receipt_print(request, pk):
    report = Report.objects.get(pk=pk)
    items = Item.objects.all().filter(report=report).order_by('itemDate')

    context = {"items": items}
    cmd_options = {
        'orientation': 'landscape',
        'margin-top': 0,
        'margin-right': 0,
        'margin-left': 0,
        'margin-bottom': 0,
    }

    pdf = PDFTemplateResponse(template='main/reportprint2.html', request=request, context=context, cmd_options=cmd_options)
    return HttpResponse(pdf.rendered_content, 'application/pdf')

@login_required
def receipt_print_single(request, pk):
    it = Item.objects.all().filter(pk=pk)
    context = {"items": it}

    cmd_options = {
        'orientation': 'landscape',
        'margin-top': 0,
        'margin-right': 0,
        'margin-left': 0,
        'margin-bottom': 0,
    }

    pdf = PDFTemplateResponse(template='main/reportprint2.html', request=request, context=context, cmd_options=cmd_options)
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
                    'main/reportdetail.html',
                    context
                )
            except Report.DoesNotExist:
                raise Http404("Raport nie istnieje!")
    return redirect('home')


@login_required
def item_add(request, rpk):
    # find report
    try:
        report = Report.objects.get(pk=rpk)
    except  Report.DoesNotExist:
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


def item_delete(request, rpk, pk):

    assert isinstance(request, HttpRequest)
    try:
        Item.objects.get(pk=pk).delete()
    except Report.DoesNotExist:
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
