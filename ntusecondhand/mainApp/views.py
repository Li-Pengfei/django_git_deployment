from django.shortcuts import render
from mainApp.forms import UserForm, UserProfileInfoForm, AddItemModelForm
from mainApp.models import ItemModel, UserProfileInfo

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
        context = super(IndexView, self).get_context_data(**kwargs)

        all_item_list = ItemModel.objects.all()
        for item in all_item_list:
            try:
                wechat = UserProfileInfo.objects.get(user=item.user).wechat
            except UserProfileInfo.DoesNotExist:
                wechat = None
            item.wechat = wechat

        context['all_item_list'] = all_item_list
        return context


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


class ManageMyItemView(TemplateView):
    template_name = 'mainApp/manageMyItem.html'

    def get_context_data(self, **kwargs):
        context = super(ManageMyItemView, self).get_context_data(**kwargs)

        # Load User Items
        user = self.request.user
        context['user_item_list'] = ItemModel.objects.filter(user=user)
        return context


class AddItemView(View):

    def post(self, request, *args, **kwargs):
        added = False
        item_form = AddItemModelForm(data=request.POST)

        if item_form.is_valid():

            item = item_form.save(commit=False)
            item.user = request.user
            item.save()

            added = True
            return render(request, 'mainApp/addItem.html', context={
                'item_form': item_form, 'added': added,
            })
        else:
            print(item_form.errors)
            item_form = AddItemModelForm()
            return render(request, 'mainApp/addItem.html', context={
                'item_form': item_form, 'added': added,
            })

    def get(self, request, *args, **kwargs):
        added = False
        item_form = AddItemModelForm()
        return render(request, 'mainApp/addItem.html', context={
            'item_form': item_form, 'added': added,
        })
