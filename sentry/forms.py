from django.forms.models import ModelForm, ModelChoiceField
from django.forms import modelformset_factory
from sentry.models import User
from people.models import Person
from dal import autocomplete


class AssignUserIdentityForm(ModelForm):

    class Meta:
        model = User
        fields = ['person']
        widgets = {
            'person': autocomplete.ModelSelect2(url='sentry:users-autocomplete')
        }


AssignUserIdentityFormset = modelformset_factory(User, AssignUserIdentityForm, extra=0)
