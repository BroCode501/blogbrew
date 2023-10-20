from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView
from .models import UserProfile, User
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

class Profile(DetailView):
    model = UserProfile  # Use the UserProfile model instead of User
    slug_field = 'user__username'  # Use the User model's username
    slug_url_kwarg = 'username'
    template_name = "profile.html"
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        # Get the User object for the given username
        user = User.objects.get(username=self.kwargs['username'])
        print(user, self.kwargs['username'])
        # Get the UserProfile associated with the User
        return UserProfile.objects.get(user=user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


from django.views.generic.edit import UpdateView

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'edit_profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)
