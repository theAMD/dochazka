from django.contrib.auth.models import AbstractUser
from django.db import models
from people.models import Person


class User(AbstractUser):
    person = models.ForeignKey(Person, null=True, blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        if self.person:
            if self.person.nickname:
                return self.person.nickname
            return self.person.__unicode__()
        return self.username
