'''
Created on Dec 3, 2017

@author: TBENER
'''

from django.db import models
from django.urls import reverse
from .entity import Entity
from random import choices

_ENTITY_DISPLAY_TYPES = [
    (0, 'Grid'),
    (1, 'Stack'),
    ]

class Section(models.Model):
    title      = models.CharField(max_length=50, help_text="Will be displayed on site.")
    help_text   = models.TextField(null=True, blank=True, help_text="Will be displayed on site.")
    entities    = models.ManyToManyField(Entity, through='EntityInSection')
    
    def __str__(self):
        return self.title
    
    def long_name(self):
        inpages = ', '.join(self.page_set.all())
        return '{title} (appears in {pages})'.format(title=self.title, pages=inpages)
    
    def pages(self):
        change_link = '<a href="#" onclick="alert(\'Not active yet\')">Add...</a>'
        page_link_template = '<a href="{link}">{name}</a>'
        return  '<br/>'.join(page_link_template.format(link=p.admin_change_url(), name=str(p)) for p in self.page_set.all()) + '<br/>' + change_link
    
    pages.allow_tags = True
    pages.short_description = 'Pages'
    
    def admin_change_url(self):
        return reverse('admin:ccenter_section_change', args=(self.id,))
    
    def name_as_link(self):
        return '<a href="{link}">{name}</a>'.format(name=self.title, link=self.admin_change_url())
    
    name_as_link.allow_tags = True
    
    class Meta:
        app_label = "ccenter"
        

#===============================================================================
# EntityInSection
# Defines how an Entity is displayed within a Section
#===============================================================================
class EntityInSection(models.Model):
    # Every Entity can exist in one or more Sections
    # One Entity can be displayed twice on the same page under different Entities, but with different fields.
    # This model defines the relationship.
    section     = models.ForeignKey(Section)
    entity      = models.ForeignKey(Entity)
    display_type = models.PositiveSmallIntegerField(choices=_ENTITY_DISPLAY_TYPES, default=0)
    starts_new_row = models.BooleanField(default=True, help_text="If True, the viewer will force new line before this entity.")
    fields      = models.ManyToManyField("Field")
    
    class Meta:
        app_label = "ccenter"
        verbose_name_plural = "Entities in Section"
        
        
