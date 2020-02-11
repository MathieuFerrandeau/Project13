"""Spent forms"""
from django.utils import timezone
from django import forms
from .models import UserOutlay

YEARS = [x for x in range(2020, 2030)]


class RecordOutlayForm(forms.ModelForm):

    class Meta:
        model = UserOutlay
        fields = ['payment_method']

    amount = forms.DecimalField(max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'placeholder': '00,00'}))
    payment_date = forms.DateField(initial=timezone.now().date(),
                                   widget=forms.SelectDateWidget(years=YEARS))


class UpdateOutlayForm(forms.ModelForm):

    class Meta:
        model = UserOutlay
        fields = ['payment_method']

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_date = forms.DateField(initial=timezone.now().date(),
                                   widget=forms.SelectDateWidget(years=YEARS))
