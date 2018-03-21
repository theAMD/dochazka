from django import forms
from models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput,
            'location': forms.TextInput,
            'calendar': forms.Select(attrs={'class': 'form-control'})
        }