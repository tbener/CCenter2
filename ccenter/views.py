from django.shortcuts import get_object_or_404, render
from .models.core import Page, EntityValueDefinition, Value
from .forms import ValueForm

# Create your views here.

# def page(request, page_id):
#     p = get_object_or_404(Page, pk=page_id)
#     
#     return render(request, 'ccenter/page.html', {'page': p})

from django.forms import inlineformset_factory, modelform_factory, modelformset_factory
from django.forms.formsets import formset_factory
from ccenter import forms

from django.forms import BaseInlineFormSet

class NonDefaultValueInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            qs = super().get_queryset().filter(is_default=False)
            self._queryset = qs
        return self._queryset
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Value.objects.filter(is_default=False)

def page(request, page_id):
    
    #ValueForm = modelform_factory(Value, exclude=('value_definition', ))
    
    
#     if request.method == 'POST':
#         formset = ValueInlineFormSet(request.POST)
#         if formset.is_valid():
#             formset.save()
            
#         form = PageForm(request.POST)
#         if form.is_valid():
#             # do some process...
#             # resirect?
#             # return HttpResponseRedirect('/thanks/')
#             pass
#     
#     else:
#         form = PageForm()
    
    ValueInlineFormSet = inlineformset_factory(EntityValueDefinition, Value, ValueForm, extra=0, formset=NonDefaultValueInlineFormSet)
    ValueFormSet = modelformset_factory(Value, ValueForm)
    
    p = get_object_or_404(Page, pk=page_id)
    
    section_list = p.sections.all()
    for section in section_list:
        ent_list = section.entities.all()
        section.entity_list = ent_list
        for entity in section.entity_list:
            vdef = entity.entityvaluedefinition_set.first()
            if vdef:
                prefix = 'value_set-%s' % entity.pk
                if request.method == 'POST':
                    formset = ValueInlineFormSet(request.POST, instance=vdef, prefix = prefix)
                    # formset.data = {k:v for k,v in formset.data.items() if k.startswith(prefix)}
                    if formset.is_valid():
                        formset.save()
                else:
                    default_values = vdef.value_set.filter(is_default=True)
                    non_default_values = vdef.value_set.filter(is_default=False)
                    
                    if not non_default_values:
                        # we create the values based on the defaults
                        
                        values_to_clone = default_values
                        if entity.entity_type == 1: # _LIST
                            values_to_clone = default_values.filter(is_selected=True)
                            # TODO: handle no is_selected=True (make one)
                        
                        for val in values_to_clone:
                            val.pk = None
                            val.is_default = False
                            val.save()
                            
                    
                            
                    formset = ValueInlineFormSet(instance=vdef, prefix = prefix)
                
                entity.values_formset = formset
    
    
    return render(request, 'ccenter/page.html', {'page': p, 'sections': section_list})




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




