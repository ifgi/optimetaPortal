from django import template

register = template.Library()

# https://stackoverflow.com/a/23783666/261210
@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)