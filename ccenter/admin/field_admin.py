'''
Created on Dec 4, 2017

@author: TBENER
'''

from ccenter.models.field import Field
from ccenter.admin.admin import BaseAdmin, ccBaseAdminTabularInline
from ccenter.models.value import Value

class ValuesInline(ccBaseAdminTabularInline):
    model = Value
    fields = ['display_value', 'char_value', 'integer_value', 'boolean_value', 'order']
    sortable_field_name = 'order'
    
    is_default = None
    
    def get_queryset(self, request):
        qs = super(ValuesInline, self).get_queryset(request)
        qs = qs.filter(is_default=self.is_default)
        return qs

class DefaultValuesInline(ValuesInline):
    is_default = True
    verbose_name_plural = 'default values'
    
class UserValuesInline(ValuesInline):
    is_default = False
    verbose_name_plural = 'user values'
        

class FieldAdmin(BaseAdmin):
    model = Field
    list_display = ['label', 'field_type']
    inlines = [DefaultValuesInline, UserValuesInline]
    list_filter = ['entity']
    
    class Media:
        js = ('admin/js/entity-value-definition.js', )

