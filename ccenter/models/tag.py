'''
Created on Dec 3, 2017

@author: TBENER
'''

from django.db import models

# The Tags are composing the treeview
class Tag(models.Model):
    name        = models.CharField(max_length=50)
    parent      = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    
    # the children of a folder (Tag) are a combination of the tags AND PAGES that linked to that Tag.
    def children(self):
        childs = list(self.tag_set.all())  # returns a list of all Tags which self is their parent
        if self.id:
            for page in self.page_set.all():
                _tag = Tag(name = page.title)
                _tag.page = page
                _tag.folder = self
                childs.append(_tag)
              
        return childs
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "ccenter"