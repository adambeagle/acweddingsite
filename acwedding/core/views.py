from django.views.generic import DetailView

from .models import Page

class PageDetailView(DetailView):
    model = Page
    
    # TODO: select_related or prefetch_related on the queryset to 
    #       minimize DB hits? See Two Scoops 12.3.3
    
