from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='slicelist')
def list_page_slice(collection, pg):
	start = pg * settings.PDF_NUMBER_OF_ITEMS_PER_PAGE
	end = start + settings.PDF_NUMBER_OF_ITEMS_PER_PAGE
	return collection[start:end]

