from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from people.forms import UploadCSVForm
from people.models import UnitType, Unit, Person
from django.template.response import TemplateResponse


class ImportCSVView(LoginRequiredMixin, FormView):
    form_class = UploadCSVForm
    template_name = 'upload_form.html'

    def form_valid(self, form):
        parentUnit = Unit()
        parentUnit.name = form.cleaned_data.get('unitName')
        parentUnit.type = form.cleaned_data.get('unitType')
        unitType = UnitType.objects.filter(weight__lt=parentUnit.type.weight).order_by('weight').first()
        imported = list()

        parentUnit.save()

        for row in str(form.cleaned_data.get('csvFile').read().decode()).split('\n'):
            row = row.split(';')
            if len(row) == 3:
                unit = Unit.objects.filter(name=row[2]).get_or_create(name=row[2], type=unitType,
                                                                      parent=parentUnit)
                person = Person()
                person.first_name = row[0]
                person.last_name = row[1]
                person.save()

                person.membership.add(unit[0])

                if unit[0] not in imported:
                    imported.append(unit[0])

        return TemplateResponse(self.request, self.template_name, {'imported': imported})
