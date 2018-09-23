from django.db import models
from datetime import datetime
from django.utils import timezone


class Calendar(models.Model):
    name = models.TextField(max_length=30)
    slug = models.SlugField(max_length=30)
    color = models.TextField(max_length=6, null=True, blank=True)
    parent = models.ForeignKey('Calendar', null=True, blank=True)
    gcal_id = models.TextField(null=True, blank=True)
    unit = models.OneToOneField('people.Unit', related_name='calendar')

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def getEvents(self, start = None, end = None):
        events = Event.objects.filter(calendar=self)
        if start:
            events.filter(start__gte=start)

        if end:
            events.filter(start__lt=end)

        return events


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.TextField(max_length=30)
    description = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    calendar = models.ForeignKey('Calendar', related_name='event_set')

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def ended(self):
        return self.end < timezone.now()

    @property
    def multiday(self):
        return self.start.date() != self.end.date()


class Participation(models.Model):
    event = models.ForeignKey("Event", related_name="participations")
    person = models.ForeignKey("people.Person")
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.event.__unicode__() + ' ' + self.person.__unicode__()

    def toggle(self):
        self.status = not self.status

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.event.ended() or force_update or self.pk is None:
            super(Participation, self).save(force_insert, force_update,
                                            using, update_fields)












