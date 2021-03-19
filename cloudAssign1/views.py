from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'root_index.html'