from django import template

from googlemaps.util import linkable_latitude, linkable_longitude

register = template.Library()

@register.filter(is_safe=True)
def linkablelatitude(value):
    """
    Alias to googlemaps.util.linkable_latitude
    """
    return linkable_latitude(value)

@register.filter(is_safe=True)
def linkablelongitude(value):
    """
    Alias to googlemaps.util.linkable_longitude
    """
    return linkable_longitude(value)

@register.inclusion_tag('googlemaps/multi_marker.html')
def multi_marker_map(multi_marker_map):
    """
    Embeds a simple Google map onto the page at the location of the 
    template tag. A simple map can contain any number of markers, 
    with customized icons and hovertext. See the SimpleMap and Marker
    classes in models.py.
    
    The Google Maps JavaScript API v3 is used to embed the map. 
    """
    return { 'map' : multi_marker_map }
    