from django.contrib import admin
from .models import Calendar, Event, Participation

admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(Participation)
