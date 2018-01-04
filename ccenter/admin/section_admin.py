'''
Created on Dec 3, 2017

@author: TBENER
'''

from ccenter.models.entity import Entity
from ccenter.models.field import Field
from ccenter.admin.admin import BaseAdmin, ccBaseAdminTabularInline
from ccenter.models.section import Section


class EntityInline(ccBaseAdminTabularInline):
    model = Section.entities.through
    fields = ['entity', 'display_type', 'starts_new_row', 'fields']    
    verbose_name = 'Entity'
    verbose_name_plural = 'Entities'


class SectionAdmin(BaseAdmin):
    model = Section
    list_display = ['title'] #, 'pages']
    inlines = [EntityInline]
    fieldsets = [
        (None,          {'fields': ['title', 'help_text', 'pages']}),
        ]
    readonly_fields = ['pages']