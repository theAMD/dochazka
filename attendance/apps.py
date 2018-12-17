from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = 'attendance'
    verbose_name = 'Attendance'

    def ready(self):
        import attendance.signals
