from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView

from .models import Accommodation, PointOfInterest
from googlemaps.models import Marker

class BasePointOfInterestIndexView(ListView):
    context_object_name = 'poi_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.model.CATEGORY_CHOICES
        
        return context
        
class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'tourisminfo/accommodation_detail.html'
    context_object_name = 'poi'
    
    def get_slug_field(self):
        return 'marker__location__slug'

class AccommodationIndexView(BasePointOfInterestIndexView):
    model = Accommodation
    template_name = 'tourisminfo/accommodations_index.html'

class PointOfInterestIndexView(BasePointOfInterestIndexView):
    model = PointOfInterest
    template_name = 'tourisminfo/poi_index.html'

class PointOfInterestDetailView(DetailView):
    model = PointOfInterest
    template_name = 'tourisminfo/poi_detail.html'
    context_object_name = 'poi'
    
    try:
        ceremony_marker = Marker.objects.get(name='ceremony')
    except ObjectDoesNotExist:
        ceremony_marker = None
        
    try:
        reception_marker = Marker.objects.get(name='reception')
    except ObjectDoesNotExist:
        reception_marker = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ceremony_marker'] = self.ceremony_marker
        context['reception_marker'] = self.reception_marker
        
        return context
        
    def get_slug_field(self):
        return 'marker__location__slug'
        
    #~ def get_object(self):
        #~ qset = self.get_queryset()
        
        #~ return qset.objects.get(marker__location__slug='')
        
