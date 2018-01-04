'''
Created on Sep 4, 2016

@author: TBENER
'''

from django.contrib import admin
from ccenter.admin.admin import BaseAdmin
from CCenter2.constants import *
from ccenter.models.page import Page

    



    

class SectionInline(admin.TabularInline):
    model = Page.sections.through
    fields = ['section', 'order']
    verbose_name = 'section'
    verbose_name_plural = 'sections'




class PageAdmin(BaseAdmin):
    model = Page
    list_display = ['title', 'sub_title']
    inlines = [SectionInline,]
    fieldsets = [
        (None,                  {'fields': ['title', 'tree_name', 'sub_title', 'tags', 'related_entity']}),
        #('More',                {'fields': ['description'], 'classes': [class_collapse]})
        ]

        