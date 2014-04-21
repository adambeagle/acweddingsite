from datetime import datetime

wedding_date = datetime(2015, 5, 16, 13)

def days_remaining_context_processor(request):
    """Context processor. Adds days_remaining to context of every view."""
    now = datetime.now()
    return {'days_remaining' : (wedding_date - now).days}