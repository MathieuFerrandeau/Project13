import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.dates import MonthArchiveView
from .forms import RecordOutlayForm
from .models import Category, Outlay, UserOutlay
# Create your views here.

@login_required
class UserOutlayArchiveMonthView(MonthArchiveView):
    """expense_history_view"""
    queryset = UserOutlay.objects.all()
    date_field = "payment_date"
    allow_future = True

@login_required
def record_outlay_view(request):

    form = RecordOutlayForm(request.POST)
    if form.is_valid():
        outlay_selected = request.POST.get('outlay_field')
        user = request.user
        outlay = Outlay.objects.get(name=outlay_selected)
        amount = form.cleaned_data['amount']
        payment_method = form.cleaned_data['payment_method']
        payment_date = form.cleaned_data['payment_date']
        UserOutlay.objects.create(user_name=user, outlay=outlay, amount=amount, payment_method=payment_method,
                                  payment_date=payment_date)
        return redirect('spent:outlay_recorded')

    else:
        form = RecordOutlayForm()
        category = Category.objects.all()
        if request.method == 'POST':
            cat_selected = request.POST.get('cat_list')
            outlay = Outlay.objects.filter(category=cat_selected)
            outlay_id = request.POST.get('outlay_list')
            if outlay_id:
                outlay_selected = Outlay.objects.get(id=outlay_id)
                cat_outlay_selected_name = outlay_selected.category.name

                return render(request, 'spent/record_outlay.html', {'categories': category,
                                                                    'cat_outlay_selected_name': cat_outlay_selected_name,
                                                                    'outlay': outlay,
                                                                    'outlay_selected': outlay_selected,
                                                                    'form': form,
                                                                    })
            elif cat_selected:
                category_choose = Category.objects.get(id=cat_selected)
                return render(request, 'spent/record_outlay.html', {'category_choose': category_choose,
                                                                    'outlay': outlay,
                                                                    })
            else:
                return render(request, 'spent/record_outlay.html', {'categories': category})

        return render(request, 'spent/record_outlay.html', {'categories': category})

def outlay_recorded_view(request):
    """outlay_recorded"""
    return render(request, 'spent/outlay_recorded.html')

def bills_view(request):
    """e"""
    if request.method == 'POST':
        form = RecordOutlayForm(request.POST)
        if form.is_valid():
            user = request.user
            outlay = Outlay.objects.get(id=213)
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            payment_date = form.cleaned_data['payment_date']
            print(user, outlay, amount, payment_date, payment_method)
            UserOutlay.objects.create(user_name=user, outlay=outlay, amount=amount, payment_method=payment_method,
                                      payment_date=payment_date)
            return redirect('spent:bills')
    else:
        form = RecordOutlayForm()

    return render(request, 'spent/bills.html', {'form': form})

def history(request):
    """outlay_recorded"""

    useroutlay = UserOutlay.objects.filter(user_name=request.user)
    mois = {'1': 'Janvier', '2': 'Février', '3': 'Mars', '4': 'Avril', '5': 'Mai', '6': 'Juin',
            '7': 'Juillet', '8': 'Août', '9': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

    month_key_selected = request.GET.get('month_list')
    #print(month_key_selected)
    if month_key_selected:
        for month in useroutlay:
            #print(month)
            user_outlaymonth = UserOutlay.objects.filter(user_name=request.user,
                                                         payment_date__month=month_key_selected,
                                                         payment_date__year=2020)
            print(user_outlaymonth)
            if len(user_outlaymonth) != 0:
                amount = 0
                for sum in user_outlaymonth:
                    amount += sum.amount
                    print('izi', amount)
                return render(request, 'spent/history.html', {'user_outlaymonth': user_outlaymonth,
                                                              'amount': amount})

            else:
                error_message = ("Aucune dépense enregistrée pour le mois de " + mois[month_key_selected] + ", renouvellez votre choix.")
                return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                              'mois': mois,
                                                              'error_message': error_message})



    return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                  'mois': mois})

"""

    if useroutlay date month exist show month (line 1)
    if click on month get month id
    show useroutlay (date=month id, user=request.user)
    if click on back show line 1
    """



