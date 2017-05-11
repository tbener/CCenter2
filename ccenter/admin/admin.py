from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin



class BaseAdmin(admin.ModelAdmin):
    pass


class dbmBaseInline(InlineModelAdmin):
    # override <extra> variable in admin inline to get the Add and Delete permissions automatically
    
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True


class dbmBaseAdminTabularInline(admin.TabularInline, dbmBaseInline):
    extra = 0

class dbmBaseAdminStackedInline(admin.StackedInline, dbmBaseInline):
    extra = 0


from ..models.core import *
from .page import PageAdmin, SectionAdmin, EntityAdmin
from .valuedefinitionadmin import EntityValueDefinitionAdmin

admin.site.register(Folder, BaseAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityValueDefinition, EntityValueDefinitionAdmin)
admin.site.register(Value, BaseAdmin)



