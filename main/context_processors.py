# -*- coding: utf-8 -*-
from django.shortcuts import reverse
from datetime import date
from attendance.models import Calendar

def menu_generator(request):
    #
    # Three level example menu
    #
    # menu = [
    #     {'icon': 'tachometer', 'url': '/', 'text': 'Home', 'submenu': None},
    #     {'icon': 'car', 'url': "#", 'text': 'transport', 'submenu': [
    #         {'icon': 'fighter-jet', 'url': "/jet", 'text': 'jet', 'submenu': []},
    #         {'icon': 'bus', 'url': "/bus", 'text': 'bus', 'submenu': []},
    #         {'icon': 'car', 'url': "#", 'text': 'cars', 'submenu': [
    #                 {'icon': 'car', 'url': "/car", 'text': 'car', 'submenu': []},
    #                 {'icon': 'taxi', 'url': "/taxi", 'text': 'taxi', 'submenu': []},
    #         ]},
    #     ]},
    #     {'icon': 'car', 'url': "#", 'text': 'transport', 'submenu': [
    #         {'icon': 'fighter-jet', 'url': "/jet", 'text': 'jet', 'submenu': []},
    #         {'icon': 'bus', 'url': "/bus", 'text': 'bus', 'submenu': []},
    #         {'icon': 'car', 'url': "#", 'text': 'cars', 'submenu': [
    #             {'icon': 'car', 'url': "/car", 'text': 'car', 'submenu': []},
    #             {'icon': 'taxi', 'url': "/taxi", 'text': 'taxi', 'submenu': []},
    #         ]},
    #     ]}
    # ]
    today = date.today()
    menu = [
        {'icon': 'tachometer', 'url': reverse('home'), 'text': 'dashing'},

    ]

    try:
        if request.user.person:
            calendars = [{
                    'icon': 'calendar',
                    'url': reverse('attendance:calendar', kwargs={'calendar_slug': 'personal'}),
                    'text': u'Můj kalendář'
                }]
            for calendar in Calendar.objects.filter(unit__in=request.user.person.member_in_units()):
                calendars.append({
                    'icon': 'calendar',
                    'url': reverse('attendance:calendar', kwargs={'calendar_slug': calendar.slug}),
                    'text': calendar.name
                })

            menu.append(
                {'icon': 'calendar', 'url': "#", 'text': u'Kalendáře', 'submenu': calendars }
            )
    except:
        pass

    return {'menu': menu}
