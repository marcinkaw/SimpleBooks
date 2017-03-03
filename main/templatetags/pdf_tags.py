from django import template
from django.conf import settings
from main.templatetags.pdf_filters import list_page_slice

register = template.Library()


def sum_list(items, direction):
	amount = 0
	for item in items:
		if direction == item.itemDirection:
			amount += item.amount

	return amount


@register.simple_tag(name='sumfolio')
def sum_folio(items, page, direction):
	sliced_items = list_page_slice(items, page)

	return sum_list(sliced_items, direction)


@register.simple_tag(name='previous_folio')
def previous_folio(items, page, direction):
	if page > 0:
		end = page * settings.PDF_NUMBER_OF_ITEMS_PER_PAGE
		sliced_items = items[:end]

		return sum_list(sliced_items, direction)

	return 0


@register.simple_tag(name='overall_sum')
def overall_sum(items, page, direction):
	end = page * settings.PDF_NUMBER_OF_ITEMS_PER_PAGE
	end += settings.PDF_NUMBER_OF_ITEMS_PER_PAGE
	sliced_items = items[:end]

	return sum_list(sliced_items, direction)
