from django import template

register = template.Library()


@register.assignment_tag(name='get_year_from_date')
def get_year_from_date(date):
	return str(date.year)


@register.assignment_tag(name='check_for_year_divider')
def check_for_year_divider(reports, current_index):
	if current_index > 0:
		report_prev_date = reports[current_index-1].fromDate
		report_current_date = reports[current_index].fromDate

		if report_prev_date.year != report_current_date.year:
			return True
		return False

	return True


