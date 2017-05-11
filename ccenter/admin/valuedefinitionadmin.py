'''
Created on Mar 9, 2017

@author: TBENER
'''

from django.contrib import admin
from .admin import dbmBaseAdminTabularInline, BaseAdmin
from ..models.core import *


class ValueInline(dbmBaseAdminTabularInline):
    model = Value
    # fields = ['section', 'order']

class EntityValueDefinitionAdmin(BaseAdmin):
    model = EntityValueDefinition
    #list_display = ('name', 'type_description')
    inlines = [ValueInline, ]

