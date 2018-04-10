from dashboard.helpers import DashboardWidget
from sentry.models import User
from django.shortcuts import render


class NewUsersDashboardWidget(DashboardWidget):
    users = None

    def __init__(self, request):
        self.request = request
        self.users = User.objects.filter(person=None).all()

    def render(self):
        return render(self.request, 'widgets/new_user_dashboard_widget.html',  {'users': self.users}).content
