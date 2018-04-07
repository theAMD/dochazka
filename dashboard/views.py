from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from context_processors import register_widgets


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomePageView, self).get_context_data()
        ctx['widgets'] = register_widgets(self.request)
        return ctx


