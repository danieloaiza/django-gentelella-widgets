import copy

from django import forms
from django.urls import reverse_lazy

from djgentelella.widgets.core import Select, update_kwargs, SelectMultiple


class BaseAutocomplete:
    def get_context(self, name, value, attrs):
        context = super().get_context(name,value,attrs)
        context['url'] = reverse_lazy(self.baseurl)
        return context


    def optgroups(self, name, value, attrs=None):
        if value and value != ['']:
            self.choices.queryset = self.choices.queryset.filter(pk__in=value)
        else:
            self.choices.queryset = self.choices.queryset.none()
        return super().optgroups(name, value, attrs=attrs)

    @property
    def media(self):
        return forms.Media( js=('gentelella/js/select2related.js', 'gentelella/js/autocompleteSelect2.js'))

class AutocompleteSelectBase(BaseAutocomplete, Select):
    template_name = 'gentelella/widgets/autocomplete_select.html'
    option_template_name = 'gentelella/widgets/select_option.html'

    def __init__(self, attrs=None, choices=(), extraskwargs=True):
        if extraskwargs:
            attrs = update_kwargs(attrs, 'AutocompleteSelect', base_class='form-control ')
        if self.baseurl is None:
            raise ValueError('Autocomplete requires baseurl to work')
        else:
            self.baseurl = self.baseurl
        attrsn = {
            'data-start_empty': 'false'
        }
        attrsn.update(attrs)
        super(AutocompleteSelectBase, self).__init__(attrsn,  choices=choices, extraskwargs=False)

class AutocompleteSelectMultipleBase(BaseAutocomplete, SelectMultiple):
    template_name = 'gentelella/widgets/autocomplete_select.html'
    option_template_name = 'gentelella/widgets/select_option.html'

    def __init__(self, attrs=None, choices=(), extraskwargs=True):
        if extraskwargs:
            attrs = update_kwargs(attrs, 'AutocompleteSelectMultiple',  base_class='form-control ')
        if self.baseurl is None:
            raise ValueError('Autocomplete requires baseurl to work')
        else:
            self.baseurl = self.baseurl
        attrsn = {
            'data-start_empty': 'false'
        }
        attrsn.update(attrs)
        super(AutocompleteSelectMultipleBase, self).__init__(attrsn, choices=choices, extraskwargs=False)

def AutocompleteSelect(url):
    class AutocompleteSelect(AutocompleteSelectBase):
        baseurl = url+"-list"

    return AutocompleteSelect

def AutocompleteSelectMultiple(url):
    class AutocompleteSelectMultiple(AutocompleteSelectMultipleBase):
        baseurl = url+"-list"
    return AutocompleteSelectMultiple
