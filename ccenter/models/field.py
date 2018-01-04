'''
Created on Dec 3, 2017

@author: TBENER
'''
from django.urls import reverse
from django.db import models
from django.forms import inlineformset_factory


_FIELD_TYPE_CHOICES = [
    ("char_value", "String"), 
    ("integer_value", "Integer"), 
    ("boolean_value", "Boolean")]

# Value definition for a single value, list, or grid column
class Field(models.Model):
    parent_field = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    label       = models.CharField(max_length=50, help_text="According to the Entity type, this will be the field label or the column header.")
    field_type  = models.CharField(max_length=50, default=_FIELD_TYPE_CHOICES[0][0], choices=_FIELD_TYPE_CHOICES)
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    is_hidden   = models.BooleanField(default=False)
    #select_from = models.ForeignKey("self", verbose_name="select from list", blank=True, null=True)  # can be used to hold the list (choices) for the parent vdef
    
    def admin_link(self):
        return '<a href="%s">%s</a>' % (reverse('admin:ccenter_field_change', args=(self.id,)), self)
    
    admin_link.short_description = ''
    admin_link.allow_tags = True
    
#     def values_formset(self):
#         ValuesFormset = inlineformset_factory(Field, Value, fields=('value_type', 'char_value', 'integer_value', 'boolean_value'), extra=0)
#         return ValuesFormset(instance = self)
    
    
    def generate_non_default_values(self):
        if not self.value_set.filter(is_default=False):
            def_values = self.value_set.filter(is_default=True)
            for val in def_values:
                val.pk = None
                val.is_default = False
                val.save()
                        
    
    def __str__(self):
        return self.label   # + " (Field)"
    
    class Meta:
        app_label = "ccenter"