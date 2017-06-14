'''
Created on Sep 4, 2016

@author: TBENER
'''

from django.contrib import admin
from .admin import dbmBaseAdminTabularInline, dbmBaseAdminStackedInline, BaseAdmin
from ..models.core import *

class EntityValueDefinitionInline(dbmBaseAdminTabularInline):
    model = EntityValueDefinition
    fields = ['admin_link']
    readonly_fields = ['admin_link']

class EntityAdmin(BaseAdmin):
    model = Entity
    list_display = ('name', 'type_description')
    inlines = [EntityValueDefinitionInline,]
    
    class Media:
        js = ('admin/js/entity.js', )
    

class SectionInline(dbmBaseAdminTabularInline):
    model = Page.sections.through
    fields = ['section', 'order']
    verbose_name = 'section'
    verbose_name_plural = 'sections'


class SectionAdminInline(dbmBaseAdminTabularInline):
    model = Section
    fields = ['title', 'description', 'order']
    readonly_fields = ['title']
    order = ['order']


class EntityInline(dbmBaseAdminTabularInline):
    model = Section.entities.through
    fields = ['entity', 'start_new_row']    
    verbose_name = 'Entity'
    verbose_name_plural = 'Entities'


class PagesInline(dbmBaseAdminTabularInline):
    model = Page.sections.through
    fields = ['page']
    
    
class SectionAdmin(BaseAdmin):
    model = Section
    list_display = ('name', 'pages')
    inlines = [EntityInline]
    fieldsets = [
        (None,          {'fields': ['name', 'help_text', 'pages']}),
        ('More',        {'fields': ['description'], 'classes': ['collapse']})
        ]
    readonly_fields = ['pages']

class PageAdmin(BaseAdmin):
    model = Page
    list_display = ['name', 'short_description']
    inlines = [SectionInline,]
    fieldsets = [
        (None,                  {'fields': ['name', 'sub_title', 'folder']}),
        ('More',                {'fields': ['description'], 'classes': ['grp-collapse grp-closed']})
        ]

class DefaultValuesInline(dbmBaseAdminTabularInline):
    model = Value
    fields = ['display_value', 'char_value', 'integer_value', 'boolean_value', 'order']
    sortable_field_name = 'order'
    
    def get_queryset(self, request):
        qs = super(DefaultValuesInline, self).get_queryset(request)
        qs = qs.filter(is_default=True)
        return qs
        

class EntityValueDefinitionAdmin(BaseAdmin):
    model = EntityValueDefinition
    list_display = ('label', 'value_type', 'entity')
    inlines = [DefaultValuesInline, ]
    list_filter = ['entity']
    
    class Media:
        js = ('admin/js/entity-value-definition.js', )


class GridRowAdmin(BaseAdmin):
    model = GridRow
    inlines = [DefaultValuesInline]
        