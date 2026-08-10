import re
from django.utils.html import escape
from .reference import resolve_reference


REFERENCE_PATTERN = re.compile(
    r"\[\[([a-zA-Z_]+):([a-zA-Z0-9_-]+)(?:\|([^]]+))?\]\]"
)


def render_references(text):
    if not text:
        return ""

    def replace(match):
        reference_type = match.group(1)
        slug = match.group(2)
        label = match.group(3)

        obj = resolve_reference(reference_type, slug)

        if obj is None:
            return escape(label or slug)

        display_text = label or str(obj)

        return (
            f'<a href="{escape(obj.get_absolute_url())}">'
            f'{escape(display_text)}'
            f'</a>'
        )

    return REFERENCE_PATTERN.sub(replace, text)