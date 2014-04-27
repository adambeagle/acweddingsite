from django.views.generic import DetailView

from .models import Page

def has_map(sections):
    """
    Return True if any Section has a non-empty and non-null 'map' attribute,
    False otherwise.
    """
    for s in sections:
        if s.map:
            return True
            
    return False

class PageDetailView(DetailView):
    queryset = Page.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['section_list'] = self.object.section_set.select_related(
            'map', 'minigallery')
        context['has_map'] = has_map(context['section_list'])
        
        return context
