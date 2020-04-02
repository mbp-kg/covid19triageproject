# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def labeltagwithcontents(value, contents):
    return value.label_tag(contents=contents)
