from django import template
from markdownx.utils import markdownify as markdownx_markdownify


register = template.Library()


@register.filter
def markdownify(value):
    return markdownx_markdownify(value)