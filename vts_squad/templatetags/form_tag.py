from django.template import Library

register = Library()

@register.filter
def label_class(v, args):
    return v.label_tag(attrs={'class':args})
@register.filter
def label_for(v, args):
    return v.label_tag(attrs={'for':args})