from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from mainApp.forms import UserForm, UserProfileInfoForm, AddItemModelForm
from mainApp.models import ItemModel, UserProfileInfo


# CBV : Class Based Views
class IndexView(TemplateView):
    template_name = 'mainApp/index.html'

    def post(self, request, *args, **kwargs):

        context = {}
        username = request.POST.get('name')
        price = request.POST.get('price')

        all_item_list = ItemModel.objects.exclude(user=username) \
            .filter(estimate_price__gte=float(price) * 0.8) \
            .filter(estimate_price__lte=float(price) * 1.2)
        electronic_item_list = []
        fashion_item_list = []
        home_item_list = []
        health_item_list = []
        baby_item_list = []
        sports_item_list = []
        grocery_item_list = []
        others_item_list = []

        for item in all_item_list:
            if item.category == 'EL':
                electronic_item_list.append(item)
            elif item.category == 'FA':
                fashion_item_list.append(item)
            elif item.category == 'HA':
                home_item_list.append(item)
            elif item.category == 'HB':
                health_item_list.append(item)
            elif item.category == 'BT':
                baby_item_list.append(item)
            elif item.category == 'SO':
                sports_item_list.append(item)
            elif item.category == 'GC':
                grocery_item_list.append(item)
            else:
                others_item_list.append(item)

            try:
                wechat = UserProfileInfo.objects.get(user=item.user).wechat
            except UserProfileInfo.DoesNotExist:
                wechat = None
            item.wechat = wechat

        context['all_item_list'] = all_item_list
        context['elec_item_list'] = electronic_item_list
        context['fash_item_list'] = fashion_item_list
        context['home_item_list'] = home_item_list
        context['heal_item_list'] = health_item_list
        context['baby_item_list'] = baby_item_list
        context['spor_item_list'] = sports_item_list
        context['groc_item_list'] = grocery_item_list
        context['othe_item_list'] = others_item_list

        return render(request, 'mainApp/index.html', context=context)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        all_item_list = ItemModel.objects.all()
        electronic_item_list = []
        fashion_item_list = []
        home_item_list = []
        health_item_list = []
        baby_item_list = []
        sports_item_list = []
        grocery_item_list = []
        others_item_list = []

        for item in all_item_list:
            if item.category == 'EL':
                electronic_item_list.append(item)
            elif item.category == 'FA':
                fashion_item_list.append(item)
            elif item.category == 'HA':
                home_item_list.append(item)
            elif item.category == 'HB':
                health_item_list.append(item)
            elif item.category == 'BT':
                baby_item_list.append(item)
            elif item.category == 'SO':
                sports_item_list.append(item)
            elif item.category == 'GC':
                grocery_item_list.append(item)
            else:
                others_item_list.append(item)

            try:
                wechat = UserProfileInfo.objects.get(user=item.user).wechat
            except UserProfileInfo.DoesNotExist:
                wechat = None
            item.wechat = wechat

        context['all_item_list'] = all_item_list
        context['elec_item_list'] = electronic_item_list
        context['fash_item_list'] = fashion_item_list
        context['home_item_list'] = home_item_list
        context['heal_item_list'] = health_item_list
        context['baby_item_list'] = baby_item_list
        context['spor_item_list'] = sports_item_list
        context['groc_item_list'] = grocery_item_list
        context['othe_item_list'] = others_item_list
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
            # registered = True
            login(request, user)
            # return render(request, 'mainApp/registration.html', context={
            #     'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
            # })
            return HttpResponseRedirect(reverse('index'))
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


class MakeOfferView(View):
    def post(self, request, *args, **kwargs):

        item = ItemModel.objects.get(pk=request.POST.get('item'))

        if item:
            return render(request, 'mainApp/make_offer.html', {"item": item})
        else:
            return HttpResponse('invalid item id')

    def get(self, request, *args, **kwargs):
        return HttpResponse('this url does not accept GET request')


class ManageMyItemView(TemplateView):
    template_name = 'mainApp/index.html'

    def get_context_data(self, **kwargs):
        context = super(ManageMyItemView, self).get_context_data(**kwargs)

        # Load User Items
        user = self.request.user
        all_item_list = ItemModel.objects.filter(user=user)
        electronic_item_list = []
        fashion_item_list = []
        home_item_list = []
        health_item_list = []
        baby_item_list = []
        sports_item_list = []
        grocery_item_list = []
        others_item_list = []

        for item in all_item_list:
            if item.category == 'EL':
                electronic_item_list.append(item)
            elif item.category == 'FA':
                fashion_item_list.append(item)
            elif item.category == 'HA':
                home_item_list.append(item)
            elif item.category == 'HB':
                health_item_list.append(item)
            elif item.category == 'BT':
                baby_item_list.append(item)
            elif item.category == 'SO':
                sports_item_list.append(item)
            elif item.category == 'GC':
                grocery_item_list.append(item)
            else:
                others_item_list.append(item)

            try:
                wechat = UserProfileInfo.objects.get(user=item.user).wechat
            except UserProfileInfo.DoesNotExist:
                wechat = None
            item.wechat = wechat

        context['all_item_list'] = all_item_list
        context['elec_item_list'] = electronic_item_list
        context['fash_item_list'] = fashion_item_list
        context['home_item_list'] = home_item_list
        context['heal_item_list'] = health_item_list
        context['baby_item_list'] = baby_item_list
        context['spor_item_list'] = sports_item_list
        context['groc_item_list'] = grocery_item_list
        context['othe_item_list'] = others_item_list
        return context


class AddItemView(View):
    def post(self, request, *args, **kwargs):
        added = False
        item_form = AddItemModelForm(data=request.POST)

        if item_form.is_valid():

            item = item_form.save(commit=False)
            item.user = request.user
            item.save()

            return HttpResponseRedirect(reverse('mainApp:manage_my_items'))
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


class MatchedItemView(View):
    def post(self, request, *args, **kwargs):

        context = {}
        item = ItemModel.objects.get(pk=request.POST.get('item'))
        context['item'] = item

        all_item_list = ItemModel.objects.exclude(pk=item.id) \
            .filter(estimate_price__gte=float(item.estimate_price) * 0.8) \
            .filter(estimate_price__lte=float(item.estimate_price) * 1.2)
        electronic_item_list = []
        fashion_item_list = []
        home_item_list = []
        health_item_list = []
        baby_item_list = []
        sports_item_list = []
        grocery_item_list = []
        others_item_list = []

        for item in all_item_list:
            if item.category == 'EL':
                electronic_item_list.append(item)
            elif item.category == 'FA':
                fashion_item_list.append(item)
            elif item.category == 'HA':
                home_item_list.append(item)
            elif item.category == 'HB':
                health_item_list.append(item)
            elif item.category == 'BT':
                baby_item_list.append(item)
            elif item.category == 'SO':
                sports_item_list.append(item)
            elif item.category == 'GC':
                grocery_item_list.append(item)
            else:
                others_item_list.append(item)

            try:
                wechat = UserProfileInfo.objects.get(user=item.user).wechat
            except UserProfileInfo.DoesNotExist:
                wechat = None
            item.wechat = wechat

        context['all_item_list'] = all_item_list
        context['elec_item_list'] = electronic_item_list
        context['fash_item_list'] = fashion_item_list
        context['home_item_list'] = home_item_list
        context['heal_item_list'] = health_item_list
        context['baby_item_list'] = baby_item_list
        context['spor_item_list'] = sports_item_list
        context['groc_item_list'] = grocery_item_list
        context['othe_item_list'] = others_item_list

        if item:
            return render(request, 'mainApp/matched_items.html', context=context)
        else:
            return HttpResponse('invalid item id')

    def get(self, request, *args, **kwargs):
        return HttpResponse('this url does not accept GET request')
