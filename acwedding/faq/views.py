from django.views.generic import ListView

from .models import Entry

class IndexView(ListView):
    template_name = 'faq/index.html'
    model = Entry
