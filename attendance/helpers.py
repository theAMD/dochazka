from datetime import datetime, timedelta
from calendar import monthrange
from attendance.models import Event, Participation
import collections
from django.db.models import Q


class MonthHelper():
    calendar = None
    slug = None
    firstDay = None
    lastDay = None

    nextMonth = None
    prevMonth = None

    def __init__(self, calendar, year, month):
        if not isinstance(calendar, list):
            self.calendar = [calendar]
            self.slug = calendar.slug
        else:
            self.calendar = calendar
            self.slug = 'personal'


        self.firstDay = datetime(year, month, 1, 0, 0, 0)
        self.lastDay = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)

        self.nextMonth = self.lastDay + timedelta(days=1)
        self.prevMonth = self.firstDay - timedelta(days=1)

    def getDays(self):

        first_day = self.firstDay - timedelta(days=self.firstDay.isoweekday())
        last_day = self.lastDay + timedelta(days=7 - self.lastDay.isoweekday())

        delta = last_day - first_day  # timedelta
        days = []
        for i in range(1, delta.days + 1, 7):
            week = collections.OrderedDict()
            for j in range(0, 7):
                day = first_day + timedelta(days=i + j)
                week[day] = Event.objects \
                    .filter(calendar__in=self.calendar, start__lte=datetime(day.year, day.month, day.day, 23, 59, 59)) \
                    .exclude(end__lte=day).order_by('start')
            days.append(week)
        return days


class EventHelper():
    event = None

    def __init__(self, event):
        self.event = event

    def getParticipations(self):
        participants = self.event.calendar.unit.get_members()
        participations = []
        for person in participants:
            p = Participation.objects.get_or_create(event=self.event, person=person,
                                                    defaults={'event': self.event, 'person': person})
            participations.append(p[0])
        return participations
