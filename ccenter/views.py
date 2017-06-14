from django.shortcuts import get_object_or_404, render
from .models.core import Page, EntityValueDefinition, Value, GridRow, Folder
from .forms import ValueForm
from django.forms import inlineformset_factory, modelformset_factory, BaseInlineFormSet

class NonDefaultValueInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            qs = super().get_queryset().filter(is_default=False)
            self._queryset = qs
        return self._queryset
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Value.objects.filter(is_default=False)




def page(request, page_id, folder_id=None):
    
    ValueInlineFormSet = inlineformset_factory(EntityValueDefinition, Value, ValueForm, extra=0, formset=NonDefaultValueInlineFormSet)
    ValueFormSet = modelformset_factory(Value, ValueForm)
    
    RowValueInlineFormSet = inlineformset_factory(GridRow, Value, ValueForm, extra=0)
    
    p = get_object_or_404(Page, pk=page_id)
    
    section_list = p.sections.all()
    for section in section_list:
        ent_list = section.entities.all()
        section.entity_list = ent_list
        for entity in section.entity_list:
            if entity.entity_type in (0, 1):
                entity.value_definitions = []
                for vdef in entity.entityvaluedefinition_set.all():
                    prefix = 'value_set-%s' % vdef.pk
                    if request.method == 'POST':
                        formset = ValueInlineFormSet(request.POST, instance=vdef, prefix = prefix)
                        # formset.data = {k:v for k,v in formset.data.items() if k.startswith(prefix)}
                        if formset.is_valid():
                            formset.save()
                    else:
                        vdef.generate_non_default_values()
                        
#                         if entity.entity_type == 2: # _GRID
#                             # only create the rows from defaults, if necessary
#                             for idx, val in enumerate(vdef.value_set.filter(is_default=False).all()):
#                                 if not val.grid_row:
#                                     val.grid_row, created = GridRow.objects.get_or_create(entity=entity, index=idx)
#                                     val.save()
#                         else:
                        
                        
                        formset = ValueInlineFormSet(instance=vdef, prefix = prefix)
                    
                    # endif POST
                    
                    vdef.values_formset = formset
                    entity.value_definitions.append(vdef)
            
               
            if entity.entity_type == 2: # _GRID
                entity.value_definitions = entity.entityvaluedefinition_set.all()
                entity.rows = entity.gridrow_set.all()
                for r in entity.rows:
                    prefix="row%s" % r.pk
                    if request.method == 'POST':
                        formset = RowValueInlineFormSet(request.POST, instance=r, prefix = prefix)
                        if formset.is_valid():
                            formset.save()
                    else:
                        formset = RowValueInlineFormSet(instance=r, prefix=prefix)
                    
                    r.values_formset = formset
    
    
    active_folder = Folder.objects.get(pk=folder_id) if folder_id else None
    
    return render(request, 'ccenter/page.html', {'page': p, 'sections': section_list, 'folders': Folder.objects.filter(parent=None), 'active_folder': active_folder})





            

def test(request):
    
    
#     ValueInlineFormSet = inlineformset_factory(ValueDefinition, Value, ValueForm, extra=0)
    
    ImageInfoFormset = modelformset_factory(Value, fields=('boolean_value', 'integer_value'), extra=0)
    
    if request.method == 'POST':
        print(request.POST.keys())
        formset = ImageInfoFormset(request.POST, prefix='form1')
        print(formset.data.keys())
        if formset.is_valid():
            formset.save()
            
        formset2 = ImageInfoFormset(request.POST, prefix='form2')
        if formset2.is_valid():
            formset2.save()
    else:
        formset = ImageInfoFormset(queryset=Value.objects.filter(pk=1), prefix='form1')
        formset2 = ImageInfoFormset(queryset=Value.objects.filter(pk=2), prefix='form2')
    
    formset_list = [formset, formset2]
    
#     formset = ValueInlineFormSet(ValueDefinition.objects.filter(pk=1))
    
       
    
    return render(request, 'ccenter/test.html', {'formset_list': formset_list})




