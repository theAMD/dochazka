from django.conf.urls import url
from attendance.views import CalendarView, EventDetailView, MonthCalendarView, ToggleParticipation, \
    PersonalCalendarView, EventCreateView, EventEditView



urlpatterns = [


    url(r'calendar/personal/(?P<year>\d{4})-(?P<month>\d{2})$', PersonalCalendarView.as_view(), name="personal"),
    url(r'calendar/(?P<calendar_slug>\w+)/(?P<year>\d{4})-(?P<month>\d{2})$', MonthCalendarView.as_view(), name="monthCalendar"),
    url(r'calendar/(?P<calendar_slug>\w+)$', CalendarView.as_view(), name="calendar"),

    url(r'event/(?P<pk>\d+)$', EventDetailView.as_view(), name='event.detail'),
    url(r'toggle/(?P<id>\d+)/$', ToggleParticipation.as_view(), name='toggleParticipation'),
    url(r'add$', EventCreateView.as_view(), name='event.create'),
    url(r'edit/(?P<pk>\d+)/$', EventEditView.as_view(), name='event.edit')

]