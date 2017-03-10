from django import template
from main.utils.pyliczba import kwotaslownie
import math

register = template.Library()


def sum_list(items, direction):
    amount = 0
    for item in items:
        if direction == item.itemDirection:
            amount += item.amount

    return amount


@register.simple_tag(name='list_page_slice')
def list_page_slice(collection, page, items_per_page):
    start = page * items_per_page
    end = start + items_per_page
    return collection[start:end]


@register.simple_tag(name='sum_single_page')
def sum_single_page(items, page, direction, items_per_page):
    sliced_items = list_page_slice(items, page, items_per_page)

    return sum_list(sliced_items, direction)


@register.simple_tag(name='sum_previous_pages')
def sum_previous_pages(items, page, direction, items_per_page):
    if page > 0:
        end = page * items_per_page
        sliced_items = items[:end]

        return sum_list(sliced_items, direction)

    return 0


@register.simple_tag(name='get_sum_from_all_pages')
def get_sum_from_all_pages(items, page, direction, items_per_page):
    end = page * items_per_page
    end += items_per_page
    sliced_items = items[:end]

    return sum_list(sliced_items, direction)


@register.filter(name='number2words')
def convert_number_to_words(number):
    return kwotaslownie(float(number))

