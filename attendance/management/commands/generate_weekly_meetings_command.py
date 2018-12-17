from django.core.management.base import BaseCommand

from attendance.models import Event
from people.models import Unit
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create weekly meetings set for given group'

    def add_arguments(self, parser):
        parser.add_argument('unit', type=str, help='Name of the unit')
        parser.add_argument('start', type=str, help='Start time')
        parser.add_argument('end', type=str, help='End date')
        parser.add_argument('-m', '--end-hours', type=str, help='Start time')
        parser.add_argument('-n', '--event-name', type=str, help='Name of the event')

    def handle(self, *args, **kwargs):
        unit = Unit.objects.filter(id=kwargs['unit']).get()
        date = datetime.strptime(kwargs['start'], '%d-%m-%Y %H:%M')
        endDate = datetime.strptime(kwargs['end'], '%d-%m-%Y %H:%M')

        counter = 0
        while date < endDate:
            event = Event()
            event.calendar = unit.calendar
            event.start = date
            event.end = datetime(year=date.year, month=date.month,
                                 day=date.day, hour=endDate.hour,
                                 minute=endDate.minute)
            event.name = kwargs.get('name', 'Schůzka - ' + unit.name)
            event.save()
            counter += 1
            date += timedelta(days=7)

        print('Created ' + str(counter) + ' occurrances of ' + event.name)
