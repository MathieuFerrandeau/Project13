from django import forms
from .models import UserOutlay

class RecordOutlayForm(forms.Form):

    class Meta:
        model = UserOutlay

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_method = forms.CharField(max_length=15)
    payment_date = forms.DateField()


