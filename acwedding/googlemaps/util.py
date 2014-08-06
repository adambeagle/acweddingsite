def linkable_latitude(value):
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
    
def linkable_longitude(value):
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