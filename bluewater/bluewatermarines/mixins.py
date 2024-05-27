from django.shortcuts import redirect
from django.urls import reverse

class LogoutRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)