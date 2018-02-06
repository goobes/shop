"""Base models"""

from django.db import models
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.urls import reverse
from uuid import uuid4
import os


STATES = (
    (u'AP', u'ANDHRA PRADESH'),
    (u'AR', u'ARUNACHAL PRADESH'),
    (u'AS', u'ASSAM'),
    (u'BR', u'BIHAR'),
    (u'CG', u'CHATTISGARH'),
    (u'DL', u'DELHI'),
    (u'GA', u'GOA'),
    (u'GJ', u'GUJARAT'),
    (u'HR', u'HARYANA'),
    (u'HP', u'HIMACHAL PRADESH'),
    (u'JK', u'JAMMU & KASHMIR'),
    (u'JS', u'JHARKHAND'),
    (u'KA', u'KARNATAKA'),
    (u'MP', u'MADHYA PRADESH'),
    (u'MH', u'MAHARASHTRA'),
    (u'MN', u'MANIPUR'),
    (u'ML', u'MEGHALAYA'),
    (u'MZ', u'MIZORAM'),
    (u'NL', u'NAGALAND'),
    (u'OR', u'ORISSA'),
    (u'PB', u'PUNJAB'),
    (u'RJ', u'RAJASTHAN'),
    (u'SK', u'SIKKIM'),
    (u'TN', u'TAMIL NADU'),
    (u'TR', u'TRIPURA'),
    (u'UK', u'UTTARAKHAND'),
    (u'UP', u'UTTAR PRADESH'),
    (u'WB', u'WEST BENGAL'),
    (u'AN', u'ANDAMAN & NICOBAR'),
    (u'CH', u'CHANDIGARH'),
    (u'DN', u'DADAR & NAGAR HAVELI'),
    (u'DD', u'DAMAN & DIU'),
    (u'LD', u'LAKSHADWEEP'),
    (u'PY', u'PONDICHERRY')
)

# from - https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
@deconstructible
class UniqueId(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

upload_unique_id = UniqueId("items")

class Item(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1024)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to=upload_unique_id, null=True, blank=True)
    instagram_url = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return u"<Item: {}-{}>".format(self.name, self.price)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField(max_length=512)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, choices=STATES)
    postal_code = models.CharField(max_length=8)
    phone_mobile = models.CharField(max_length=13)
    phone_landline = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return u"<Profile: {}>".format(self.user)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk': self.id})


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_id = models.CharField(max_length=64)
    payment_request_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    fees = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    longurl = models.URLField()
    shorturl = models.URLField()
    status = models.CharField(max_length=16)
