from django.db import models
from django.core.validators import MinValueValidator

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
    name        = models.CharField(max_length=50, help_text="A unique explanatory name. Will not be displayed on site.")
    header      = models.CharField(max_length=50, help_text="Will be displayed on site.")
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    description = models.TextField(null=True, blank=True, help_text="Internal. Will not be displayed on site.")
    
    class Meta:
        abstract = True
        app_label = "ccenter"

class Folder(models.Model):
    name        = models.CharField(max_length=50)
    parent      = models.ForeignKey("Folder", null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "ccenter"


class Page(BaseModel):
    folder      = models.ForeignKey("Folder")
    sub_title   = models.CharField(max_length=100, null=True, blank=True)
    sections    = models.ManyToManyField("Section", through='SectionInPage')
    
    def short_description(self):
        sections_count = self.sections.count()
        return ', '.join(s.header for s in self.sections.all()) if self.sections else 'No sections'
    
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
        return '{name} (appears in {pages})'.format(name=self.header, pages=inpages)
    
    def pages(self):
        return ', '.join(str(p) for p in self.page_set.all())
    
    class Meta:
        app_label = "ccenter"
    
# Properties of a Section within a page that can be different for the same section on different pages.     
class SectionInPage(models.Model):
    page        = models.ForeignKey(Page)
    section     = models.ForeignKey(Section)
    order       = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        app_label = "ccenter"

class Entity(BaseModel):
    # An Entity is a representation of data. It could be a single value, a list, or a grid
    entity_type  = models.IntegerField(verbose_name="type", choices=_ENTITY_TYPE_CHOICES, default=0) 
    
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
        
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


class GridRow(models.Model):
    
    entity      = models.ForeignKey(Entity)
    index       = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s (%s)" % (self.index, self.entity)
    
    class Meta:
        app_label = "ccenter"
        #unique_together = ("entity", "index")


# TODO: add an optional Help Text field (need it for grid column)
# Value definition for a single value, list, or grid column
class EntityValueDefinition(models.Model):
    # This Model is used to define the value of the Entity, according to its type.
    # If the Entity is of type Single Value or a List, then one EntityValueDefinition instance will represent it.
    # If the Entity is of type Grid, then each instance of EntityValueDefinition represents a column.
    # If the type is List or Grid, then multiple Values will be related to each EntityValueDefinition.
    entity      = models.ForeignKey("Entity", null=True)
    label       = models.CharField(max_length=50, help_text="According to the Entity type, this will be the field label or the column header.")
    order       = models.PositiveSmallIntegerField(default=0, help_text="For grid.")
    attribute   = models.CharField(max_length=50, null=True, help_text="To identify the value by the consumers")
    value_type  = models.CharField(max_length=50, default=_FIELD_TYPE_CHOICES[_SINGLE_VALUE][0], choices=_FIELD_TYPE_CHOICES)
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    is_hidden   = models.BooleanField(default=False)
    
    def values_formset(self):
        ValuesFormset = inlineformset_factory(EntityValueDefinition, Value, fields=('value_type', 'char_value', 'integer_value', 'boolean_value'), extra=0)
        return ValuesFormset(instance = self)
    
    def __str__(self):
        return self.label   # + " (EntityValueDefinition)"
    
    class Meta:
        app_label = "ccenter"

       
class Value(models.Model):
    # This model represents the actual field value.
    # Every Value references to a single EntityValueDefinition,
    # but in case of List or Grid, multiple values will reference a single EntityValueDefinition.
    value_definition    = models.ForeignKey("EntityValueDefinition")
    grid_row            = models.ForeignKey(GridRow, null=True)
    is_default          = models.BooleanField(default=True)    # shouldn't be presented. in admin=True, otherwise=False
    order               = models.PositiveSmallIntegerField(default=0, null=True, blank=True)   # for grid or list
    display_value       = models.CharField(max_length=200, null=True, blank=True, help_text="Used for list item display")
    # value_type          = models.CharField(max_length=50, default=_FIELD_TYPE_CHOICES[0][0], choices=_FIELD_TYPE_CHOICES)
    char_value          = models.CharField(max_length=200, null=True, blank=True)
    integer_value       = models.IntegerField(null=True, blank=True)        #, validators=[MinValueValidator(5)])
    boolean_value       = models.BooleanField()
    value_field         = models.CharField(max_length=20, blank=True, null=True)
    is_selected         = models.BooleanField(default=False)    # used for selection from list (dropdown)
    
    
    
#     def choices(self):
#         if self.value_definition.entity.value_type == _LIST:
#             l = self.value_definition.value_set.filter(is_default=True)
#             return [(getattr(v, v.actual_field_value), v.display_value) for v in l]
#             
#         return None
#     
#     integer_value.choices = choices

    # this will be used in the template
    def value_type(self):
        return self.value_definition.value_type
    
    def actual_field_value(self):
        return getattr(self, self.value_type(), self.char_value)
    
    def is_list(self):
        return self.value_definition.entity.entity_type == _LIST
    
    def __str__(self):
        return str(self.value_definition) + ('[{0}]'.format(self.order) if self.order else "") + " (%s Value)" % "Default " if self.is_default else ""
    
    class Meta:
        app_label = "ccenter"


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














