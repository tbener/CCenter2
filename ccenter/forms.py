'''
Created on Jun 30, 2016

@author: TBENER
'''
from django import forms
from django.forms import inlineformset_factory
from django.utils.functional import curry
from ccenter.models import Value, EntityValueDefinition
from django.forms.models import BaseModelFormSet



class ValueForm(forms.ModelForm):
    
#     def actual_field(self):
#         return getattr(self, self.instance.value_type())
    
    class Meta:
        model = Value
        exclude = ['value_field']
        
    def __init__(self, *args, **kwargs):
        super(ValueForm, self).__init__(*args, **kwargs)
        if not self.instance.is_default:
            val = self.instance
            if self.instance.is_list():
                list_items = val.value_definition.value_set.filter(is_default=True)
                ch = [(v.actual_field_value(), v.display_value) for v in list_items]
                self.fields[val.value_type()].widget = forms.Select(choices=ch)



FIELD_TYPES = {
    "char_value" : forms.CharField,
    "integer_value" : forms.IntegerField,
    "boolean_value" : forms.BooleanField,
    "select_value" : forms.Select,
    "char_value" : forms.DateInput,
    "text_value" : curry(forms.CharField, widget=forms.Textarea)
               }

# 
# class PageForm(forms.ModelForm):
#     
#     class Meta:
#         model = Page
#         fields = ['name', 'sub_title', 'description']
#         
#         
class BaseValueFormSet(BaseModelFormSet):
     
     
    def __init__(self, *args, **kwargs):
        super(BaseValueFormSet, self).__init__(*args, **kwargs)
        self.queryset = Value.objects.filter(value_definition='O')
        


class ValueFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(ValueFormSet, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Value
        exclude = ('value_field',)



def entity_values_formset(entity):
    if entity.value_type == 0:    # single value
        vdef = entity.valuedefinition_set.first()
        return vdef_values_formset(vdef)
        

    return None

# def vdef_values_formset(vdef):
#     if vdef:
#         val = vdef.value_set.first()
#         if val:
#             fields = {'value_field': FIELD_TYPES[val.value_type]()}
#             fields['value_field'].initial = val.actual_field()
#             ValueForm = type('ValueFormForm', (BaseValueForm,), fields)
#             ValuesFormset = inlineformset_factory(EntityValueDefinition, Value, ValueForm, extra=0)
#             return ValuesFormset(instance=vdef)
#             
#     return None








