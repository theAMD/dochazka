from django.conf.urls import url, include
from dashboard.views import HomePageView


urlpatterns = [
    url(r'$', HomePageView.as_view(), name='home')
]