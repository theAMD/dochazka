from django.contrib import admin
from people.models import Person, Unit, UnitType

admin.site.register(Person)
admin.site.register(Unit)
admin.site.register(UnitType)
