'''
Created on Nov 30, 2017

@author: TBENER
'''

from django.db import models
from django.urls import reverse
from ccenter.models.entity import Entity
from ccenter.models.tag import Tag
from ccenter.models.section import Section

class Page(models.Model):
    title      = models.CharField(max_length=50, help_text="Page title.")
    tree_name  = models.CharField(max_length=50, help_text="To be used in the tree. Leave empty to use the Title", null=True, blank=True)
    sub_title   = models.CharField(max_length=100, null=True, blank=True)
    tags      = models.ManyToManyField(Tag)
    sections    = models.ManyToManyField(Section, through='SectionInPage')
    related_entity = models.ForeignKey(Entity, null=True, blank=True) # if related_object exist, Page will derive some properties from it. 
    
    
    def admin_change_url(self):
        return reverse('admin:ccenter_page_change', args=(self.id,))
    
    def get_absolute_url(self):
        return reverse('ccenter:page', args=[str(self.id)])
    
    def get_tree_name(self):
        return self.tree_name or self.title
    
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = "ccenter"
        
        
# Properties of a Section within a page that can be different for the same section on different pages.     
class SectionInPage(models.Model):
    page        = models.ForeignKey(Page)
    section     = models.ForeignKey(Section)
    order       = models.PositiveIntegerField(default=0)
    
    class Meta:
        app_label = "ccenter"