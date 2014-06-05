from django import template

register = template.Library()

@register.filter(is_safe=True)
def linkablelatitude(value):
    """
    Append proper direction to a float represented latitude.
    
    Example:
      In: 45.06112
      Out: 45.06112N
    """
    value = float(value)
    direction = 'N' if value > 0 else 'S'
    value = abs(value)
    
    return '{0}{1}'.format(value, direction)

@register.filter(is_safe=True)
def linkablelongitude(value):
    """
    Append proper direction to a float represented longitude.
    
    Example:
      In: -83.472899
      Out: 83.472899W
    """
    value = float(value)
    direction = 'E' if value > 0 else 'W'
    value = abs(value)
    
    return '{0}{1}'.format(value, direction)

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
    