from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Page, SubheaderImage

def has_map(sections):
    """
    Return True if any Section has a non-empty and non-null 'map' attribute,
    False otherwise.
    """
    for s in sections:
        if s.map:
            return True
            
    return False
    
class ContactView(FormView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('core:contact_thanks')
    form_class = ContactForm
    
    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        return super().form_valid(form, *args, **kwargs)

class PageDetailView(DetailView):
    queryset = Page.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # MiniGalleryImages are not prefetched to avoid hitting the DB for 
        # them at all if a page does not include any minigalleries.
        context['subheader_image'] = SubheaderImage.objects.get(
            page_id=self.object.pk)
        context['section_list'] = self.object.section_set.select_related(
            'map', 'minigallery', 'sectionaudio_set', )
        context['has_map'] = has_map(context['section_list'])
        
        return context
