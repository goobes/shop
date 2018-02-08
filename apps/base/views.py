"""Views for the base app"""

from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from instamojo_wrapper import Instamojo
from datetime import datetime
import logging
import hmac
import hashlib

from .models import Profile, Item, Payment
from .forms import ProfileForm

logger = logging.getLogger(__name__)

if settings.INSTAMOJO['TEST']:
    payment_api = Instamojo(api_key=settings.INSTAMOJO['API_KEY'],
        auth_token=settings.INSTAMOJO['AUTH_TOKEN'],
        endpoint='https://test.instamojo.com/api/1.1/')
else:
    payment_api = Instamojo(api_key=settings.INSTAMOJO['API_KEY'],
        auth_token=settings.INSTAMOJO['AUTH_TOKEN'])

def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')

def check_profile(request):
    if Profile.objects.filter(user__username=request.user):
        return redirect('home')
    else:
        return redirect('profile-create')

@login_required
def make_payment(request, pk):
    item = Item.objects.get(pk=pk)
    payment = Payment.objects.create(
            user=request.user,
            item=item,
            payment_at=datetime.now(),
            amount=item.price)
    response = payment_api.payment_request_create(
            amount=item.price,
            purpose=item.name,
            send_email=True,
            email=request.user.email,
            redirect_url=request.build_absolute_uri(reverse('payment-redirect', kwargs={'pk': payment.id})),
            webhook=request.build_absolute_uri(reverse('payment-webhook'))
            )
    if response['success']:
        payment.payment_request_id = response['payment_request']['id']
        payment.save()
    else:
        logger.error("make_payment: payment gateway failed: %s" % response['message'])
    return render(request, 'base/payment_create.html',
                    {
                    'item': item,
                    'payment': payment,
                    'response': response
                    }
                )

@login_required
def payment_redirect(request, pk):
    payment = Payment.objects.get(pk=pk)
    payment.payment_id = request.GET.get("payment_id")
    payment.payment_request_id = request.GET.get("payment_request_id")
    payment.save()

    logger.info("payment_redirect: payment_id - {}".format(payment.payment_id))
    logger.info("payment_redirect: payment_request_id - {}".format(payment.payment_request_id))
    return render(request, 'base/payment_complete.html')

@csrf_exempt
def payment_webhook(request):
    data = request.POST.dict()
    mac = data.pop("mac")
    message = message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
    mac_calculated = hmac.new(settings.INSTAMOJO['SALT'].encode(), message.encode(), hashlib.sha1).hexdigest()
    logger.info("payment_webhook: mac - {}".format(mac))
    logger.info("payment_webhook: calculated mac - {}".format(mac_calculated))
    if mac_calculated == mac:
        payment = Payment.objects.get(payment_request_id=data['payment_request_id'])
        payment.payment_id = data['payment_id']
        #payment.payment_request_id = data['payment_request_id']
        payment.status = data['status']
        payment.fees = data['fees']
        payment.longurl = data['longurl']
        payment.shorturl = data['shorturl']
        payment.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


#TODO - Add redirect from dispatch if Profile already exists - redirect to Profile Update
class ProfileCreate(CreateView):
    model = Profile
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileDetail(DetailView):
    model = Profile

class ItemList(ListView):
    model = Item

class ItemDetail(DetailView):
    model = Item
