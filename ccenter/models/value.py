'''
Created on Dec 3, 2017

@author: TBENER
'''

from django.db import models
from ccenter.models.field import Field
from ccenter.models.instance import Instance
from ccenter.models.entity import Entity

class Value(models.Model):
    # This model represents the actual field value.
    # Every Value references to a single Field.
    field    = models.ForeignKey(Field)
    #entity      = models.ForeignKey(Entity, through=Instance)
    instance            = models.ForeignKey(Instance, null=True, blank=True, on_delete=models.CASCADE)
    is_default          = models.BooleanField(default=True)    # shouldn't be presented. in admin=True, otherwise=False
    display_value       = models.CharField(max_length=200, null=True, blank=True, help_text="Used for list item display")
    char_value          = models.CharField(max_length=200, null=True, blank=True)
    integer_value       = models.IntegerField(null=True, blank=True)        #, validators=[MinValueValidator(5)])
    boolean_value       = models.BooleanField()
    order               = models.PositiveIntegerField(default=0, null=True, blank=True)   # for list
    is_selected         = models.BooleanField(default=False)    # used for selection from list (dropdown)
    
    
    
    # this will be used in the template
    def value_type(self):
        return self.field.field_type
    
    def actual_field_value(self):
        return getattr(self, self.value_type(), self.char_value)
    
#     def is_list(self):
#         return self.value_definition.entity.entity_type == _LIST
    
    # choices returns 2 variables: True if there are choices (more than one). and the choices as a list.
    def choices(self):
        if self.field.select_from:
            list_items = self.field.select_from.value_set.all()
            ch = [(v.actual_field_value(), v.display_value) for v in list_items]
            return len(ch)>1, ch
        return False, None
    
    def __str__(self):
        val = self.display_value or str(self.actual_field_value())
        if self.is_default:
            val += " (Default)"
        return val
    
    class Meta:
        app_label = "ccenter"
        ordering = ['order']