'''
Created on Sep 4, 2016

@author: TBENER
'''

from django.contrib import admin
from .admin import dbmBaseAdminTabularInline, dbmBaseAdminStackedInline, BaseAdmin
from ..models.core import *

class ExtendedPropertiesAdminInline(dbmBaseAdminStackedInline):
    model = ExtendedProperties
    exclude = ('section',)
    extra = 1

class EntityAdmin(BaseAdmin):
    model = Entity
    list_display = ('name', 'type_description')
    inlines = [ExtendedPropertiesAdminInline,]

class SectionInline(dbmBaseAdminTabularInline):
    model = Page.sections.through
    fields = ['section', 'order']


class SectionAdminInline(dbmBaseAdminTabularInline):
    model = Section
    fields = ['title', 'description', 'order']
    readonly_fields = ['title']
    order = ['order']


class EntityInline(dbmBaseAdminTabularInline):
    model = Section.entities.through
    fields = ['entity', 'start_new_row']    


class PagesInline(dbmBaseAdminTabularInline):
    model = Page.sections.through
    fields = ['page']
    
    
class SectionAdmin(BaseAdmin):
    model = Section
    list_display = ('name', 'pages')
    inlines = [EntityInline, PagesInline]

class PageAdmin(BaseAdmin):
    model = Page
    list_display = ['name', 'short_description']
    inlines = [SectionInline,]

class ValueInline(dbmBaseAdminTabularInline):
    model = Value
    # fields = ['section', 'order']

class EntityValueDefinitionAdmin(BaseAdmin):
    model = EntityValueDefinition
    #list_display = ('name', 'type_description')
    inlines = [ValueInline, ]


class GridRowAdmin(BaseAdmin):
    model = GridRow
    inlines = [ValueInline]
        