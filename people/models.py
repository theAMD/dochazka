# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    membership = models.ManyToManyField("Unit", related_name="members")

    @property
    def name(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def member_in_units(self):
        member_in = []
        for unit in self.membership.all():
            if unit not in member_in:
                member_in.append(unit)
                member_in = member_in + unit.get_parents()
            continue
        return member_in


class Unit(models.Model):
    name = models.CharField(max_length=60)
    number = models.CharField(max_length=10, blank=True, null=True)
    parent = models.ForeignKey("Unit", blank=True, null=True)
    type = models.ForeignKey("UnitType")
    leaders = models.ManyToManyField('Person', related_name='leader_in', blank=True)

    def get_members_list(self):
        members = list(self.members.all())
        for group in Unit.objects.filter(parent=self):
            members.extend(group.get_members())
        return members

    def get_members(self):
        members = list(self.members.all())
        for group in Unit.objects.filter(parent=self):
            members = list(set(members)|set(group.get_members()))
        return members

    def get_parents(self):
        parents = []
        if self.parent is not None:
            parents.append(self.parent)
            parents.extend(self.parent.get_parents())
        return parents

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.type.name)


class UnitType(models.Model):
    name = models.CharField(max_length=30)
    weight = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s (%d)" % (self.name, self.weight)
