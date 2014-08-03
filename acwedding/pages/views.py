from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from .forms import ContactForm
#~ from .models import Page, SubheaderImage
    
class ContactView(FormView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('core:contact_thanks')
    form_class = ContactForm
    
    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        return super().form_valid(form, *args, **kwargs)

#~ class PageDetailView(DetailView):
    #~ queryset = Page.objects.all()
    
    #~ def get_context_data(self, **kwargs):
        #~ context = super().get_context_data(**kwargs)
        
        #~ # MiniGalleryImages are not prefetched to avoid hitting the DB for 
        #~ # them at all if a page does not include any minigalleries.
        #~ try:
            #~ context['subheader_image'] = SubheaderImage.objects.filter(
                #~ page_id=self.object.pk)[0]
        #~ except IndexError:
            #~ context['subheader_image'] = None
        #~ context['section_list'] = self.object.section_set.select_related(
            #~ 'map', 'minigallery', 'sectionaudio_set', 
        #~ )
        #~ context = self._set_section_context(context)
        
        #~ return context
        
    #~ def _set_section_context(self, context):
        #~ """
        #~ Set the 'has_map' and 'has_minigallery' context variables and return context.
        #~ """
        #~ has_map = False
        #~ has_minigallery = False
        
        #~ for s in context['section_list']:
            #~ if has_map and has_minigallery:
                #~ break
                
            #~ if s.map is not None:
                #~ has_map = True
            
            #~ try:
                #~ # WARNING: hasattr does NOT behave as described in documentation.
                #~ # Raises DoesNotExist when it should return False.
                #~ if hasattr(s, 'minigallery'):
                    #~ has_minigallery = True
            
            #~ # WARNING: Excepting s.DoesNotExist does NOT work as expected.
            #~ # The base ObjectDoesNotExist must be used instead.
            #~ except ObjectDoesNotExist:
                #~ pass

        #~ context['has_map'] = has_map
        #~ context['has_minigallery'] = has_minigallery
        
        #~ return context
