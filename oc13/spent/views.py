import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecordOutlayForm, UpdateOutlayForm
from .models import Category, Outlay, UserOutlay


# Create your views here.


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


@login_required
def history(request):
    """outlay_recorded"""

    useroutlay = UserOutlay.objects.filter(user_name=request.user)
    date = datetime.datetime.now()
    print(date.year)
    mois = {'1': 'Janvier', '2': 'Février', '3': 'Mars', '4': 'Avril', '5': 'Mai', '6': 'Juin',
            '7': 'Juillet', '8': 'Août', '9': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

    month_key_selected = request.GET.get('month_list')
    # print(month_key_selected)
    if month_key_selected:
        for month in useroutlay:
            # print(month)
            user_outlaymonth = UserOutlay.objects.filter(user_name=request.user,
                                                         payment_date__month=month_key_selected,
                                                         payment_date__year=date.year)
            print(user_outlaymonth)
            if len(user_outlaymonth) != 0:
                mois = mois[month_key_selected]
                amount = 0
                for sum in user_outlaymonth:
                    amount += sum.amount
                    print('izi', amount)
                return render(request, 'spent/history.html', {'user_outlaymonth': user_outlaymonth,
                                                              'mois': mois,
                                                              'date': date,
                                                              'amount': amount})

            else:
                error_message = ("Aucune dépense enregistrée pour le mois suivant : " + mois[
                    month_key_selected] + ", renouvellez votre choix.")
                return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                              'mois': mois,
                                                              'date': date,
                                                              'error_message': error_message})

    return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                  'date': date,
                                                  'mois': mois})


@login_required
def outlay_modification_view(request, outlay_id):
    outlay_selected = UserOutlay.objects.get(id=outlay_id)
    print(outlay_selected.amount)
    form = UpdateOutlayForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            payment_date = form.cleaned_data['payment_date']
            print(amount, payment_date, payment_method)
            UserOutlay.objects.filter(id=outlay_id).update(amount=amount, payment_method=payment_method,
                                                           payment_date=payment_date)
            outlay_selected = UserOutlay.objects.get(id=outlay_id)
            success_message = "Modifications prises en compte."
            return render(request, 'spent/outlay_modification.html', {'outlay_selected': outlay_selected,
                                                                      'form': form,
                                                                      'success_message': success_message})

    else:
        form = UpdateOutlayForm(
            initial={
                "amount": outlay_selected.amount,
                "payment_date": outlay_selected.payment_date,
                "payment_method": outlay_selected.payment_method,
            }
        )
        return render(request, 'spent/outlay_modification.html', {'outlay_selected': outlay_selected,
                                                                  'form': form})


@login_required
def deleted_outlay_view(request, outlay_id):
    """outlay_recorded"""
    outlay_selected = UserOutlay.objects.get(id=outlay_id)
    print(outlay_selected)
    if request.method == 'POST':
        bouton_selected = request.POST.get('bouton_selected')
        print(bouton_selected)
        if bouton_selected == "1":
            print('izi')
            UserOutlay.objects.filter(id=outlay_id).delete()
            delete = True
            return render(request, 'spent/deleted_outlay.html', {'delete': delete})
    print('bizi')
    return render(request, 'spent/deleted_outlay.html', {'outlay_selected': outlay_selected})
