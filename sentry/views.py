from allaccess.models import Provider
from allaccess.views import OAuthCallback, OAuthRedirect
from django.contrib.auth import get_user_model, views, mixins
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, UpdateView
from people.models import Person
from sentry.forms import AssignUserIdentityFormset, AssignUserIdentityForm
from sentry.models import User
from dal import autocomplete
from django.db.models import Q


class LoginView(views.LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        ctx = super(LoginView, self).get_context_data()
        ctx['auth_providers'] = Provider.objects.exclude(consumer_key=None, consumer_secret=None)
        return ctx


class WPProviderCallbackView(OAuthCallback):
    provider_id = 'ID'

    def get_or_create_user(self, provider, access, info):
        "Create a shell auth.User."
        User = get_user_model()
        kwargs = {
            User.USERNAME_FIELD: provider.name + '_' + info['user_login'],
            'email': info['user_email'],
            'password': None
        }
        return User.objects.create_user(**kwargs)


class WPProviderRedirect(OAuthRedirect):
    def get_callback_url(self, provider):
        "Return the callback url for this provider."
        return reverse('sentry:callback', kwargs={'provider': provider.name})


class AssignUsersFormView(mixins.LoginRequiredMixin, FormView):
    template_name = 'assignusers_form.html'
    success_url = '/'

    def get_form(self, form_class=None):
        if self.kwargs.get('user_id', False):
            form = AssignUserIdentityForm(instance=User.objects.filter(id=self.kwargs['user_id']).get(),
                                          **self.get_form_kwargs())
        else:
            form = AssignUserIdentityFormset(queryset=User.objects.filter(person=None), **self.get_form_kwargs())

        return form

    def get_context_data(self, **kwargs):
        ctx = super(AssignUsersFormView, self).get_context_data()
        if self.kwargs.get('user_id', False):
            ctx['user_id'] = self.kwargs['user_id']
        return ctx

    def form_valid(self, form):
        form.save()
        return super(AssignUsersFormView, self).form_valid(form )

class UnassignedUserView(TemplateView):
    template_name = "unassigned.html"


class AssignUserAutocomplete(mixins.LoginRequiredMixin, autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            qs = Person.objects.all()
        else:
            # TODO: make this shit fucking work
            qs = Person.objects.filter(Q(membership__unit__in=self.request.user.person.membership.all()))

        if self.q:
            qs = qs.filter(Q(first_name__startswith=self.q) | Q(last_name__startswith=self.q))

        return qs
