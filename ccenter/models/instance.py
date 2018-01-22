'''
Created on Dec 19, 2017

@author: TBENER
'''


from django.urls import reverse
from django.db import models
from ccenter.models.entity import Entity

"""
An Instance always belongs to an Entity.
It is used for objects such as table rows or even entities that can be referenced in the tree as pages (e.g. EHR objects).
An Instance encapsulate a banch of Value objects (so a Value has a foreign key to Instance, and to a Field)  
"""
class Instance(models.Model):
    entity      = models.ForeignKey(Entity, on_delete=models.CASCADE)
    #value       = models.ForeignKey(Entity, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s %d" % (self.entity.instance_prefix or "Instance", self.id)
    
    class Meta:
        app_label = "ccenter"


