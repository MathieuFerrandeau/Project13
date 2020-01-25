from django import forms
from .models import Outlay

class RecordOutlayForm(forms.Form):

    class Meta:
        model = Outlay
        fields = ['amount', 'payment_method', 'payment_date']

