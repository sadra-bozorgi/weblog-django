from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value):
    if not value:
        return ""
    try:
        return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y/%m/%d ⏰ %H:%M')
    except:
        return value
