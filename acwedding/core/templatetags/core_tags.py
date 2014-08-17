import re
from os.path import splitext as pathsplitext

from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter

from core import util

register = template.Library()
    
# Courtesy of 
# vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
@register.filter()
def addwidgetcss(field, css):
   return field.as_widget(attrs={"class" : css})

@register.filter(is_safe=True, name='reverseurls')
@stringfilter
def reverse_urls(value):
    """Alias to core.util.reverse_urls; see documentation for original function."""
    return util.reverse_urls(value)

@register.filter(name='rsttotable')
@stringfilter
def rst_to_table(value):
    """
    Alias to core.util.rst_to_table; see documentation for original function.
    """
    return util.rst_to_table(value)
    
@register.filter(is_safe=True)
@stringfilter
def splitext(value):
    """
    Return a filename sans extension. Alias to os.splitext. 
    """
    return pathsplitext(value)[0]
