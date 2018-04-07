import abc


class DashboardWidget(object):
    request = None

    def __init__(self, request):
        return

    @abc.abstractmethod
    def render(self):
        return
