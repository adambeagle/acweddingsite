from django.views.generic import DetailView, ListView

from .models import PointOfInterest
from googlemaps.models import Marker

class AttractionsIndexView(ListView):
    template_name = 'tourisminfo/attractions_index.html'
    model = PointOfInterest
    context_object_name = 'poi_list'
    
class POIDetailView(DetailView):
    template_name = 'tourisminfo/detail.html'
    model = PointOfInterest
    context_object_name = 'poi'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ceremonyMarker'] = Marker.objects.get(pk='church')
        context['receptionMarker'] = Marker.objects.get(pk='reception')
        
        return context