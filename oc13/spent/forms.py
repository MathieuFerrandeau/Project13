from django import forms
from .models import UserOutlay

class RecordOutlayForm(forms.Form):

    class Meta:
        model = UserOutlay

    years = [x for x in range(2018, 2030)]
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_method = forms.ChoiceField(choices=(("Virement", ("Virement")), ("Prélèvement", ("Prélèvement")), ("Chèque", ("Chèque"))))
    payment_date = forms.DateField(initial="2020-01-01", widget=forms.SelectDateWidget(years=years))


