from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.decorators.csrf import csrf_protect

from .forms import ProfileEditForm, ProfileRegisterForm, ProfileLoginForm
from .models import Profile

class ProfileRegisterView(CreateView):
    model = User
    form_class = ProfileRegisterForm
    template_name = 'userprofile/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('userprofile:detail', args=(request.user.profile.id,)))

        return super(ProfileRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.form = form
        return super(ProfileRegisterView, self).form_valid(self.form)

    def get_success_url(self):
        return reverse('userprofile:detail', args=(self.form.instance.id,))

class ProfileDetailView(DetailView):
    model = Profile

class ProfileLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'userprofile/login.html'
    authentication_form = ProfileLoginForm

# Fix CSRF logout vulnerability
# I wonder why it isn't implemented by default ?
class ProfileLogoutView(CsrfViewMiddleware, LogoutView):
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Redirect users not logged in
        if request.method != 'POST' and request.user.is_authenticated:
            return self._reject(request, 'Must be a POST request')

        return super(ProfileLogoutView, self).dispatch(request, *args, **kwargs)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name_suffix = '_edit'

    def test_func(self):
        return self.request.user.profile.id == self.kwargs['pk'] or self.request.user.is_superuser
