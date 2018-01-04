'''
Created on Dec 3, 2017

@author: TBENER
'''
from ccenter.models.entity import Entity
from ccenter.models.field import Field
from ccenter.admin.admin import BaseAdmin, ccBaseAdminTabularInline
from ccenter.models.section import Section

class FieldsInline(ccBaseAdminTabularInline):
    model = Entity.fields.through
    fields = ['field']
    verbose_name_plural = "Fields"
    verbose_name ="field"
    

class SectionsInline(ccBaseAdminTabularInline):
    model = Section.entities.through
    fields = ['section']
    verbose_name_plural = "Sections"
    verbose_name ="section"




class EntityAdmin(BaseAdmin):
    model = Entity
    list_display = ['title']
    fields = ['title', 'sub_title', 'parent_entity']
    inlines = [FieldsInline, SectionsInline]
    
    class Media:
        js = ('admin/js/entity.js', )