from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Page, Section
from core.util import NonDBImage

class ContactView(FormView):
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('core:contact_thanks')
    form_class = ContactForm
    subheader_image = NonDBImage(
        static_path='images/subheaders/stan.png',
        alt_text='Stan',
        caption="Watch Dog With a Blog Fridays on Disney Channel"
    )
    
    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        return super().form_valid(form, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subheader_image'] = self.subheader_image
        
        return context
        
class PageDetailView(DetailView):
    template_name = 'pages/page_detail.html'
    model = Page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # TODO select_related? needs tests
        context['sections'] = self.object.section_set.all() 
        context['subheader_image'] = self.object.subheader_image
        
        return context
