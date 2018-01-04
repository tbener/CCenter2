from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from ccenter.models.tag import Tag
from ccenter.models.page import Page
from ccenter.models.section import Section
from ccenter.models.entity import Entity
from ccenter.models.field import Field
from ccenter.models.value import Value



class BaseAdmin(admin.ModelAdmin):
    pass


class dbmBaseInline(InlineModelAdmin):
    # override <extra> variable in admin inline to get the Add and Delete permissions automatically
    
    def has_add_permission(self, request):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True


class ccBaseAdminTabularInline(admin.TabularInline, dbmBaseInline):
    extra = 0

class ccBaseAdminStackedInline(admin.StackedInline, dbmBaseInline):
    extra = 0


# Those imports use the classes above, so they must be imported after them
from ccenter.admin.page_admin import PageAdmin
from ccenter.admin.section_admin import SectionAdmin
from ccenter.admin.entity_admin import EntityAdmin
from ccenter.admin.field_admin import FieldAdmin


admin.site.register(Tag, BaseAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Field, FieldAdmin)




