from django.views.generic import ListView

from .models import Entry

class IndexView(ListView):
    template_name = 'faq/index.html'

    def get_queryset(self):
        """Return all FAQ entries."""
        return Entry.objects.order_by('id')
