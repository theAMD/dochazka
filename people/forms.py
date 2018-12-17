from django import forms
from people.models import UnitType


class UploadCSVForm(forms.Form):
    unitName = forms.CharField()
    unitType = forms.ModelChoiceField(queryset=UnitType.objects.all())
    csvFile = forms.FileField()
