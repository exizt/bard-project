import markdown as Markdown
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings


register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def markdown(value):
    # 기본 내장 확장 기능 : 'nl2br', 'fenced_code', 'tables'
    # 외부 확장 기능
    #   - 'mdx_breakless_lists' : 'pip install mdx-breakless-lists'
    extensions = ['nl2br', 'fenced_code', 'tables', 'mdx_breakless_lists']
    return mark_safe(Markdown.markdown(value, extensions=extensions))

@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
