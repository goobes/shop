""" forms """

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'state', 'postal_code', 'phone_mobile', 'phone_landline']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 24})
        }
