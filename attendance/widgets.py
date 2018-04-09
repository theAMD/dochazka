from dashboard.helpers import DashboardWidget
from attendance.models import Event
from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import render

class NextEventDashboardWidget(DashboardWidget):
    user = None
    events = None
    reuest = None

    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.events = Event.objects.filter(calendar__unit__members__in=[self.user.person])\
            .filter(Q(end__gte=datetime.now()) | Q(start__lte=datetime.now(), end__gte=datetime.now()))\
            .order_by('end').distinct().all()
        self.firstEventIsToday = False
        if len(self.events) > 0:
            if self.events[0].start.date() == datetime.today().date():
                self.firstEventIsToday = True


    def render(self):
        return render(self.request, 'widgets/next_event_widget.html', {'events': self.events, 'firstEventIsToday': self.firstEventIsToday}).content
