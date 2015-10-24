import os
from django.conf import settings
from django.template import Library

from django_dri import RESP_IMG_BREAKPOINTS

register = Library()


@register.filter
def resp_img(img):
    img = img.name
    breakpoints = RESP_IMG_BREAKPOINTS
    filename, ext = os.path.splitext(img)
    sources = []
    if ext == '.gif':
        return ''
    for breakpoint in breakpoints:
        sources.append("{media_url}{fn}-{size}{ext} {width}w, ".format(
            media_url=settings.MEDIA_URL,
            fn=filename,
            size=breakpoint,
            ext=ext,
            width=breakpoint
        ))
    return ' '.join(sources)
