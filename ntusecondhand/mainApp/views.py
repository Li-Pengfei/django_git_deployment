import googlemaps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from mainApp.forms import UserForm, UserProfileInfoForm, AddItemModelForm
from mainApp.models import ItemModel, UserProfileInfo, Offer


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
        all_item_list = []
        if request.user.is_authenticated:
            all_item_list = ItemModel.objects.filter(user=request.user)

        if item:
            return render(request, 'mainApp/make_offer.html', {"item": item, "all_item_list": all_item_list})
        else:
            return HttpResponse('invalid item id')

    def get(self, request, *args, **kwargs):
        return HttpResponse('this url does not accept GET request')


class AddOfferView(View):
    def post(self, request, *args, **kwargs):

        target_item = ItemModel.objects.get(pk=request.POST.get('target_item'))
        offer_type = request.POST.get('offer_type')
        offer_item = None
        offer_status = 'ON'
        if offer_type == 'EX':
            offer_item = ItemModel.objects.get(pk=request.POST.get('offer_item'))
            Offer.objects.create(initiator=offer_item, receiver=target_item, offer_type=offer_type,
                                 offer_status=offer_status)
        else:
            Offer.objects.create(receiver=target_item, offer_type=offer_type, offer_status=offer_status)
        return HttpResponseRedirect(reverse('mainApp:manage_my_offers'))

    def get(self, request, *args, **kwargs):
        return HttpResponse('this url does not accept GET request')


class ManageMyOfferView(View):

    def prepare_context(self, request):
        context = {}

        googlemap_client = googlemaps.Client('AIzaSyBWzBAHevgilfjYaEvt4LjhKI5eJWasEwk')
        held_items = ItemModel.objects.filter(user=request.user)

        incoming_offers = Offer.objects.filter(receiver__in=held_items)
        outgoing_offers = Offer.objects.filter(initiator__in=held_items)

        for in_offer in incoming_offers:
            in_user_address = "Singapore " + UserProfileInfo.objects.get(user=in_offer.initiator.user).postal_code
            out_user_address = "Singapore " + UserProfileInfo.objects.get(user=in_offer.receiver.user).postal_code

            distance_matrix = googlemap_client.distance_matrix(in_user_address, out_user_address)
            in_offer.distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']

        for out_offer in outgoing_offers:
            in_user_address = "Singapore " + UserProfileInfo.objects.get(user=out_offer.initiator.user).postal_code
            out_user_address = "Singapore " + UserProfileInfo.objects.get(user=out_offer.receiver.user).postal_code

            distance_matrix = googlemap_client.distance_matrix(in_user_address, out_user_address)
            out_offer.distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']

        context['incoming_offers'] = incoming_offers
        context['outgoing_offers'] = outgoing_offers
        return context

    def post(self, request, *args, **kwargs):

        offer_id = request.POST.get('offer_id')
        offer = Offer.objects.get(pk=offer_id)
        offer.offer_status = request.POST.get('status')
        offer.save()

        context = self.prepare_context(request)
        return render(request, 'mainApp/manage_offers.html', context=context)

    def get(self, request, *args, **kwargs):
        context = self.prepare_context(request)
        return render(request, 'mainApp/manage_offers.html', context=context)


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
