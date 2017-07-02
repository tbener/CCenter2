from django.db import models
from django.core.validators import MinValueValidator
from django.forms import inlineformset_factory

_SINGLE_VALUE = 0
_LIST = 1
_GRID = 2

_ENTITY_TYPE_CHOICES = [
        (_SINGLE_VALUE, "Single Value"),
        (_LIST, "List"),
        (_GRID, "Grid")
    ]

_FIELD_TYPE_CHOICES = [
        ("char_value", "String"),
        ("integer_value", "Integer"),
        ("boolean_value", "Boolean"),
    ]

_LIST_TYPE_CHOICES = [
        (0, "Listbox"),
        (1, "Dropdown"),
        (2, "Radio buttons"),
        (2, "Checkboxes"),
    ]

_FIELD_TYPE_CHOICES_DICT = dict((k, v) for k, v in _FIELD_TYPE_CHOICES)

# a base class for main entities (page, section, entity...)
# abstract - will not stand alone as a table in the database.
class BaseModel(models.Model):
    name        = models.CharField(max_length=50)
    header      = models.CharField(max_length=50, help_text="Will be displayed on site.")
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    description = models.TextField(null=True, blank=True, help_text="Internal. Will not be displayed on site.")
    
    class Meta:
        abstract = True
        app_label = "ccenter"

class Folder(models.Model):
    name        = models.CharField(max_length=50)
    parent      = models.ForeignKey("Folder", null=True, blank=True)
    
    # the subfolders of a folder are a combination of the folders AND PAGES that linked to that folder.
    def subfolders(self):
        sf = list(self.folder_set.all())  # returns a list of all folder which self is their parent
        if self.id:
            for page in self.page_set.all():
                f = Folder(name = page.name)
                f.page = page
                f.folder = self
                sf.append(f)
              
        return sf
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "ccenter"

from django.urls import reverse

class Page(BaseModel):
    folder      = models.ManyToManyField("Folder")
    sub_title   = models.CharField(max_length=100, null=True, blank=True)
    sections    = models.ManyToManyField("Section", through='SectionInPage')
    
    def section_links(self):
        return ' | '.join(s.name_as_link() for s in self.sections.all()) if self.sections else 'No sections'
    
    section_links.allow_tags = True
    section_links.short_description = "sections"
    
    def admin_change_url(self):
        return reverse('admin:ccenter_page_change', args=(self.id,))
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "ccenter"
        

class Section(BaseModel):
    parent_section = models.ForeignKey("Section", null=True, blank=True)
    entities    = models.ManyToManyField("Entity", through='EntityInSection')
    
    def __str__(self):
        return self.name
    
    def long_name(self):
        inpages = ', '.join(self.page_set.all())
        return '{name} (appears in {pages})'.format(name=self.name, pages=inpages)
    
    def pages(self):
        change_link = '<a href="#" onclick="alert(\'Not active yet\')">Add...</a>'
        page_link_template = '<a href="{link}">{name}</a>'
        return  '<br/>'.join(page_link_template.format(link=p.admin_change_url(), name=str(p)) for p in self.page_set.all()) + '<br/>' + change_link
    
    pages.allow_tags = True
    pages.short_description = 'Pages'
    
    def admin_change_url(self):
        return reverse('admin:ccenter_section_change', args=(self.id,))
    
    def name_as_link(self):
        return '<a href="{link}">{name}</a>'.format(name=self.name, link=self.admin_change_url())
    
    name_as_link.allow_tags = True
    
    class Meta:
        app_label = "ccenter"
    
# Properties of a Section within a page that can be different for the same section on different pages.     
class SectionInPage(models.Model):
    page        = models.ForeignKey(Page)
    section     = models.ForeignKey(Section)
    order       = models.PositiveIntegerField(default=0)
    
    class Meta:
        app_label = "ccenter"

_ENTITY_SINGLE_TYPE_CHOICES = [
    (0, 'Default'),
    (1, 'Drop down'),
    (2, 'Radio Buttons'),
    ]

_ENTITY_LIST_TYPE_CHOICES = [
    (0, 'Default'),
    (1, 'Check boxes'),
    ]

class Entity(BaseModel):
    # An Entity is a representation of data. It could be a single value, a list, or a grid
    entity_type             = models.IntegerField(verbose_name="type", choices=_ENTITY_TYPE_CHOICES, default=0) 
    single_value_options    = models.IntegerField(verbose_name="show as", choices=_ENTITY_SINGLE_TYPE_CHOICES, default=0)
    list_value_options      = models.IntegerField(verbose_name="show as", choices=_ENTITY_LIST_TYPE_CHOICES, default=0)
    list_grid_allow_add     = models.BooleanField(verbose_name="allow add", default=True)
    list_grid_allow_delete  = models.BooleanField(verbose_name="allow delete", default=True)
    list_grid_min           = models.IntegerField(verbose_name="minimum items", default=0)
    list_grid_max           = models.IntegerField(verbose_name="maximum items", default=None, blank=True, null=True, help_text="Leave blank for no limit.")
    
    def type_description(self):
        
#         global _FIELD_TYPE_CHOICES_DICT
    
        # Grid
        if self.entity_type == _GRID:
            return _ENTITY_TYPE_CHOICES[_GRID][1]
        
        val_type = 'Unknown'
        if self.entityvaluedefinition_set.exists():
            # Single value type - return the type
            val_type = _FIELD_TYPE_CHOICES_DICT[self.entityvaluedefinition_set.first().value_type]
            
        # List
        if self.entity_type == _LIST:
            return "List of type %s" % val_type
        
        return val_type
    
    def verify_default_values(self):
        if self.entity_type == _GRID:
            # we need to compute the Grid Rows in conjunction with the Columns
            # GridRow - EntityValueDefinition
            pass
        
    def generate_non_default_values(self):
        if self.entity_type == _GRID:
            vdef_list = self.entityvaluedefinition_set.all()
            if Value.objects.filter(value_definition__in = vdef_list).filter(is_default = False):
                return
            # get number of rows by column (vdef) with max values
            row_num = 0
            for vdef in vdef_list:
                row_num = max(row_num, vdef.value_set.filter(is_default=True).count())

            # get the existing rows
            rows = list(self.gridrow_set.filter(is_default=True).order_by('order'))
            # add missing rows
            for i in range(len(rows), row_num):
                rows.append(GridRow(entity=self, is_default=True))
            # set order for all
            for i, r in enumerate(rows):
                r.order = i
                r.save()
                
            # for every column (vdef) go over the values and attach it to a row
            for vdef in self.entityvaluedefinition_set.all():
                # todo: handle a vdef with not enough values (we took the max)
                for index, val in enumerate(vdef.value_set.order_by('order')):
                    val.order = index
                    val.grid_row = rows[index]
                    val.save()
            
            #####
            # on that point we should have the default values arranged
            #####
            
            # starting to create values. we assume no non-default values exist 
            for r in rows:
                non_def_row = r
                # create and save a non-default row
                non_def_row.pk = None
                non_def_row.is_default = False
                non_def_row.save()
                for v in r.value_set.all():
                    v.pk = None
                    v.grid_row = non_def_row
                    v.save()
                
            
            
                
    def __str__(self):
        return "{} ({})".format(self.name, self.type_description()) 
    
    class Meta:
        app_label = "ccenter"
        verbose_name_plural = "entities"
        

#===============================================================================
# EntityInSection
#===============================================================================
class EntityInSection(models.Model):
    # Every Entity can exist in one or more Sections
    # Need to ensure that one Entity doesn't exist twice on the same page
    # This model defines the relationship.
    # The order of an entity is within its section, this is why the row\col fields is part of this model and not the 'Entity' model
    section     = models.ForeignKey(Section)
    entity      = models.ForeignKey(Entity)
    start_new_row = models.BooleanField(default=True, help_text="If false, the viewer will force new line before this entity.")
    
    class Meta:
        app_label = "ccenter"
        verbose_name_plural = "Entities in Section"
        



class GridRow(models.Model):
    
    entity          = models.ForeignKey(Entity)
    order           = models.IntegerField(default=0)
    is_default      = models.BooleanField(default=True)    # shouldn't be presented. in admin=True, otherwise=False
    
    def __str__(self):
        return "%s (%s)" % (self.order, self.entity)
    
    def get_or_create_non_default(self):
        r, created = GridRow.objects.get_or_create(is_default=False, order=self.order, entity=self.entity)
        return r
    
    class Meta:
        app_label = "ccenter"
        #unique_together = ("entity", "index")


# Value definition for a single value, list, or grid column
class EntityValueDefinition(models.Model):
    # This Model is used to define the value of the Entity, according to its type.
    # If the Entity is of type Single Value or a List, then one EntityValueDefinition instance will represent it.
    # If the Entity is of type Grid, then each instance of EntityValueDefinition represents a column.
    # If the type is List or Grid, then multiple Values will be related to each EntityValueDefinition.
    entity      = models.ForeignKey("Entity", null=True, blank=True)
    label       = models.CharField(max_length=50, help_text="According to the Entity type, this will be the field label or the column header.")
    order       = models.PositiveIntegerField(default=0, help_text="For grid.")
    attribute   = models.CharField(max_length=50, null=True, blank=True, help_text="To identify the value by the consumers")
    value_type  = models.CharField(max_length=50, default=_FIELD_TYPE_CHOICES[_SINGLE_VALUE][0], choices=_FIELD_TYPE_CHOICES)
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    is_hidden   = models.BooleanField(default=False)
    select_from = models.ForeignKey("EntityValueDefinition", verbose_name="select from list", blank=True, null=True)  # can be used to hold the list (choices) for the parent vdef
    
   
    def admin_link(self):
        return '<a href="%s">%s</a>' % (reverse('admin:ccenter_entityvaluedefinition_change', args=(self.id,)), self)
    
    admin_link.short_description = ''
    admin_link.allow_tags = True
    
    def values_formset(self):
        ValuesFormset = inlineformset_factory(EntityValueDefinition, Value, fields=('value_type', 'char_value', 'integer_value', 'boolean_value'), extra=0)
        return ValuesFormset(instance = self)
    
    
    def generate_non_default_values(self):
        if not self.value_set.filter(is_default=False):
            def_values = self.value_set.filter(is_default=True)
            for val in def_values:
                val.pk = None
                val.is_default = False
                val.save()
                        
    
    def __str__(self):
        return self.label   # + " (EntityValueDefinition)"
    
    class Meta:
        app_label = "ccenter"

       
class Value(models.Model):
    # This model represents the actual field value.
    # Every Value references to a single EntityValueDefinition,
    # but in case of List or Grid, multiple values will reference a single EntityValueDefinition.
    value_definition    = models.ForeignKey("EntityValueDefinition")
    grid_row            = models.ForeignKey(GridRow, null=True, blank=True)
    is_default          = models.BooleanField(default=True)    # shouldn't be presented. in admin=True, otherwise=False
    order               = models.PositiveIntegerField(default=0, null=True, blank=True)   # for grid or list
    display_value       = models.CharField(max_length=200, null=True, blank=True, help_text="Used for list item display")
    char_value          = models.CharField(max_length=200, null=True, blank=True)
    integer_value       = models.IntegerField(null=True, blank=True)        #, validators=[MinValueValidator(5)])
    boolean_value       = models.BooleanField()
    value_field         = models.CharField(max_length=20, blank=True, null=True)
    is_selected         = models.BooleanField(default=False)    # used for selection from list (dropdown)
    
    
    
    # this will be used in the template
    def value_type(self):
        return self.value_definition.value_type
    
    def actual_field_value(self):
        return getattr(self, self.value_type(), self.char_value)
    
    def is_list(self):
        return self.value_definition.entity.entity_type == _LIST
    
    # choices returns 2 variables: True if there are choices (more than one). and the choices as a list.
    # choices are used in 2 cases:
    # 1. Single value with multiple defaults
    # 2. Grid - a columns can be represented by choices
    def choices(self):
        if self.value_definition.select_from:
            list_items = self.value_definition.select_from.value_set.all()
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


# TBD
class ExtendedProperties(models.Model):
    # The purpose of this class is to describe the behavior of a Section or Entity on the screen.
    # E.g. whether the user can add an object.
    section     = models.ForeignKey(Section, null=True, blank=True)
    entity      = models.ForeignKey(Entity, null=True, blank=True)
    
    allow_add       = models.BooleanField(default=True)
    allow_delete    = models.BooleanField(default=True)
    
    list_type       = models.PositiveSmallIntegerField(choices=_LIST_TYPE_CHOICES, default=1)
    multi_select    = models.BooleanField(default=False)
    
    class Meta:
        app_label = "ccenter"














