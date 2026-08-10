from django import template
from core.reference_renderer import render_references

register = template.Library()


@register.filter
def lore_links(value):
    return render_references(value)