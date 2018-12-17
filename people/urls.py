from django.conf.urls import url, include
from people.views import ImportCSVView

urlpatterns = [
    url(r'import/csv$', ImportCSVView.as_view(), name='importCsv')
]
