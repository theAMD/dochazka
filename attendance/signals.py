from people.models import Unit
from attendance.models import Calendar
from django.db.models.signals import post_save
from django.dispatch import receiver
import unidecode


@receiver(post_save, sender=Unit)
def create_calendar_on_unit_save(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        calendar = Calendar()
        calendar.unit = instance
        calendar.name = instance.name
        # TODO: this should provide unique slug
        calendar.slug = unidecode.unidecode(instance.name).lower()
        if instance.parent:
            calendar.parent = instance.parent.calendar
        calendar.save()
