from django.shortcuts import render
from mainApp.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View, TemplateView


# CBV : Class Based Views
class IndexView(TemplateView):
    template_name = 'mainApp/index.html'

    def get_context_data(self, **kwargs):
        pass


class RegisterView(View):

    def post(self, request, *args, **kwargs):
        registered = False
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
            return render(request, 'mainApp/registration.html', context={
                'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
            })
        else:
            print(user_form.errors, profile_form.errors)
            user_form = UserForm()
            profile_form = UserProfileInfoForm()
            return render(request, 'mainApp/registration.html', context={
                'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
            })

    def get(self, request, *args, **kwargs):
        registered = False
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        return render(request, 'mainApp/registration.html', context={
            'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
        })


class UserLogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserLoginView(View):

    def post(self, request, *args, **kwargs):

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse('invalid login details supplied')

    def get(self, request, *args, **kwargs):
        return render(request, 'mainApp/login.html', {})

