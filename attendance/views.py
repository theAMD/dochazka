from django.views.generic import DetailView, ListView, RedirectView, CreateView, UpdateView
from attendance.models import Calendar, Event, Participation
from .helpers import MonthHelper, EventHelper
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from forms import EventForm
from datetime import datetime


from people.models import Unit

class CalendarView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        today =  datetime.today()
        print self.kwargs
        return reverse('attendance:monthCalendar', kwargs={'calendar_slug': self.kwargs['calendar_slug'], 'year': today.strftime('%Y'), 'month': today.strftime('%m')})


class PersonalCalendarView(ListView):
    model = Calendar
    template_name = 'calendar/month.html'

    def get_context_data(self, **kwargs):
        ctx = super(PersonalCalendarView, self).get_context_data()
        ctx['month'] = MonthHelper(list(self.get_queryset()), int(self.kwargs['year']), int(self.kwargs['month']))
        return ctx

    def get_queryset(self):
        units = self.request.user.person.member_in_units()
        return Calendar.objects.filter(unit__in=units)


class MonthCalendarView(LoginRequiredMixin, DetailView):
    model = Calendar
    slug_url_kwarg = 'calendar_slug'
    template_name = 'calendar/month.html'

    def get_context_data(self, **kwargs):
        ctx = super(MonthCalendarView, self).get_context_data()
        ctx['month'] = MonthHelper(self.get_object(), int(self.kwargs['year']), int(self.kwargs['month']))
        return ctx


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(EventDetailView, self).get_context_data()
        ctx['helper'] = EventHelper(self.get_object())
        return ctx


class ToggleParticipation(LoginRequiredMixin, RedirectView):
    url = None

    def get(self, request, *args, **kwargs):
        
        participation = Participation.objects.filter(pk=self.kwargs['id']).get()
        participation.toggle()
        participation.save()
        return super(ToggleParticipation, self).get(request)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.GET.get('back', '/')


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm

    template_name = 'event_edit.html'

    def get_success_url(self):
        calendar = Calendar.objects.filter(pk=self.request.POST.get('calendar')).get()
        return reverse("attendance:monthCalendar", kwargs={'calendar_slug': calendar.slug, 'year': self.object.start.year, 'month': self.object.start.strftime("%m")})

    # def form_valid(self, form):
    #     form.save()
    #     return super(EventCreateView, self).form_valid(form)


class EventEditView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_edit.html'

    def get_success_url(self):
        calendar = Calendar.objects.filter(pk=self.request.POST.get('calendar')).get()
        return reverse("attendance:monthCalendar", kwargs={'calendar_slug': calendar.slug, 'year': self.object.start.strftime("%Y"), 'month': self.object.start.strftime("%m")})
