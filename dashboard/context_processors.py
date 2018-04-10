from attendance.widgets import NextEventDashboardWidget
from people.widgets import NewUsersDashboardWidget


def register_widgets(request):
    return [NextEventDashboardWidget(request), NewUsersDashboardWidget(request)]
