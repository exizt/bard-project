import markdown as Markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def markdown(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(Markdown.markdown(value, extensions=extensions))