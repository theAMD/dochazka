from django.shortcuts import redirect, reverse


class AssignedUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.person is not None or \
                    request.path.startswith(reverse('admin:index')) or \
                    request.path.startswith(reverse('sentry:login')):
                return self.get_response(request)
            return redirect(reverse('sentry:unassigned'))
        else:
            redirect(reverse('sentry:login'))

        return self.get_response(request)

