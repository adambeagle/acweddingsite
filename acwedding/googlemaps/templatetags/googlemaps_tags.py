from django import template

register = template.Library()

@register.inclusion_tag('googlemaps/simple.html')
def simple_map(map):
    """
    Embeds a simple Google map onto the page at the location of the 
    template tag. A simple map can contain any number of markers, 
    with customized icons and hovertext. See the SimpleMap and Marker
    classes in models.py.
    
    The Google Maps JavaScript API v3 is used to embed the map. 
    
    """
    return { 'map' : map }
    