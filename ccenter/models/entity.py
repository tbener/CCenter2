'''
Created on Nov 27, 2017

@author: TBENER
'''

from django.urls import reverse
from django.db import models
from ccenter.models.field import Field

class Entity(models.Model):
    title           = models.CharField(max_length=50, help_text="")
    sub_title       = models.CharField(max_length=100, null=True, blank=True)
    parent_entity   = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    fields          = models.ManyToManyField(Field)
    instance_prefix = models.CharField(max_length=50, help_text="")
    
    
    def admin_change_url(self):
        return reverse('admin:ccenter_entity_change', args=(self.id,))
    
    def get_absolute_url(self):
        return reverse('ccenter:entity', args=[str(self.id)])
    
    def __str__(self):
        return self.title or "Entity %d" % self.id
    
    class Meta:
        app_label = "ccenter"


