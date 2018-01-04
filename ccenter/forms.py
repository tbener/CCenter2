# '''
# Created on Jun 30, 2016
# 
# @author: TBENER
# '''
from django import forms
from django.utils.functional import curry
from django.forms.models import BaseModelFormSet
 
from ccenter.models.field import Field 
from ccenter.models.value import Value
# 
# 
# class EntityValueDefinitionForm(forms.ModelForm):
#     
#     def __init__(self, *args, **kwargs):
#         super(EntityValueDefinitionForm, self).__init__(*args, **kwargs)
#         # TODO: set queryset to get only vdefs that can be used as lists.
#         #self.fields['select_from'].quesryset = EntityValueDefinition.objects.filter(value_set)
#     
#     class Meta:
#         model = EntityValueDefinition
#         fields = ['entity', 'label', 'attribute', 'value_type', 'select_from', 'help_text']
# 
# 
class ValueForm(forms.ModelForm):
     
#     def actual_field(self):
#         return getattr(self, self.instance.value_type())
     
    class Meta:
        model = Value
        exclude = ['value_field', 'value_definition']
         
    def __init__(self, *args, **kwargs):
        super(ValueForm, self).__init__(*args, **kwargs)
         
        # if this value should be selected from list, then we need to change the widget of the 
        #    correct field to Select.
        if not self.instance.is_default:
            #if self.instance.
            has_choices, choices = self.instance.choices()
            if has_choices:
                self.fields[self.instance.value_type()].widget = forms.Select(choices=choices)
# 
# 
# 
# FIELD_TYPES = {
#     "char_value" : forms.CharField,
#     "integer_value" : forms.IntegerField,
#     "boolean_value" : forms.BooleanField,
#     "select_value" : forms.Select,
#     "char_value" : forms.DateInput,
#     "text_value" : curry(forms.CharField, widget=forms.Textarea)
#                }
# 
# # 
# # class PageForm(forms.ModelForm):
# #     
# #     class Meta:
# #         model = Page
# #         fields = ['name', 'sub_title', 'description']
# #         
# #         
# class BaseValueFormSet(BaseModelFormSet):
#      
#      
#     def __init__(self, *args, **kwargs):
#         super(BaseValueFormSet, self).__init__(*args, **kwargs)
#         self.queryset = Value.objects.filter(value_definition='O')
#         
# 
# 
# class ValueFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super(ValueFormSet, self).__init__(*args, **kwargs)
#         
#     class Meta:
#         model = Value
#         exclude = ('value_field',)
# 
# 
# 
# def entity_values_formset(entity):
#     if entity.value_type == 0:    # single value
#         vdef = entity.valuedefinition_set.first()
#         return vdef_values_formset(vdef)
#         
# 
#     return None
# 
# # def vdef_values_formset(vdef):
# #     if vdef:
# #         val = vdef.value_set.first()
# #         if val:
# #             fields = {'value_field': FIELD_TYPES[val.value_type]()}
# #             fields['value_field'].initial = val.actual_field()
# #             ValueForm = type('ValueFormForm', (BaseValueForm,), fields)
# #             ValuesFormset = inlineformset_factory(EntityValueDefinition, Value, ValueForm, extra=0)
# #             return ValuesFormset(instance=vdef)
# #             
# #     return None
# 
# 
# 
# 
# 
# 


