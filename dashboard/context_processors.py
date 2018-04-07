from attendance.widgets import NextEventDashboardWidget
from people.widgets import NewUsersDasboardWidget


def register_widgets(request):
    return [NextEventDashboardWidget(request), NewUsersDasboardWidget(request)]
