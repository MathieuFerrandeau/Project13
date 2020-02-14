import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from decimal import Decimal
from .forms import RecordOutlayForm, UpdateOutlayForm
from .models import Category, Outlay, UserOutlay


# Create your views here.


@login_required
def record_outlay_view(request):
    """Manage the outlay record for an user"""
    form = RecordOutlayForm(request.POST)
    if form.is_valid():
        outlay_selected = request.POST.get('outlay_field')
        user = request.user
        outlay = Outlay.objects.get(name=outlay_selected)
        amount = form.cleaned_data['amount']
        payment_method = form.cleaned_data['payment_method']
        payment_date = form.cleaned_data['payment_date']
        UserOutlay.objects.create(user_name=user,
                                  outlay=outlay,
                                  amount=amount,
                                  payment_method=payment_method,
                                  payment_date=payment_date)
        return redirect('spent:outlay_recorded')

    else:
        form = RecordOutlayForm()
        category = Category.objects.all()
        if request.method == 'POST':
            cat_selected = request.POST.get('cat_list')
            outlay = Outlay.objects.filter(category=cat_selected)
            outlay_id = request.POST.get('outlay_list')
            if outlay_id:  # if an outlay was chosen after the category
                outlay_selected = Outlay.objects.get(id=outlay_id)
                cat_outlay_selected_name = outlay_selected.category.name

                return render(request, 'spent/record_outlay.html', {'categories': category,
                                                                    'cat_outlay_selected_name': cat_outlay_selected_name,
                                                                    'outlay': outlay,
                                                                    'outlay_selected': outlay_selected,
                                                                    'form': form,
                                                                    })
            elif cat_selected:  # if a category was chosen
                category_choose = Category.objects.get(id=cat_selected)
                return render(request, 'spent/record_outlay.html', {'category_choose': category_choose,
                                                                    'outlay': outlay,
                                                                    })

        return render(request, 'spent/record_outlay.html', {'categories': category})


@login_required
def outlay_recorded_view(request):
    """Confirm an outlay record"""
    return render(request, 'spent/outlay_recorded.html')


@login_required
def history(request):
    """Allows users to have their spending history"""
    useroutlay = UserOutlay.objects.filter(user_name=request.user)
    if useroutlay.exists() is False:
        return redirect('spent:empty_useroutlay')
    else:
        date = datetime.datetime.now()
        mois = {'01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril', '05': 'Mai', '06': 'Juin',
                '07': 'Juillet', '08': 'Août', '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

        month_selected = request.GET.get('month_list')
        if month_selected:
            user_outlaymonth = UserOutlay.objects.filter(user_name=request.user,
                                                         payment_date__month=month_selected)
            if len(user_outlaymonth) != 0:
                return redirect('spent:history_categories', month_selected)

            else:
                error_message = ("Aucune dépense enregistrée pour le mois suivant : " + mois[month_selected] + ", renouvellez votre choix.")

                return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                              'mois': mois,
                                                              'date': date,
                                                              'error_message': error_message})

    return render(request, 'spent/history.html', {'outlay': useroutlay,
                                                  'date': date,
                                                  'mois': mois})


@login_required
def history_categories_view(request, month_selected):
    """shows total amount by categories"""

    mois = {'01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril', '05': 'Mai', '06': 'Juin',
            '07': 'Juillet', '08': 'Août', '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

    mois = mois[month_selected]
    date = datetime.datetime.now()

    user_outlaymonth = UserOutlay.objects.filter(user_name=request.user,
                                                 payment_date__month=month_selected) \
                                         .distinct("outlay__category")
    data = {}
    for categories in user_outlaymonth:
        categories_amount = UserOutlay.objects.filter(user_name=request.user,
                                                      outlay__category__name=categories.outlay.category.name)\
            .aggregate(category_amount=Sum('amount'))
        data[categories.outlay.category.name] = categories_amount['category_amount']

    total_amount = 0
    for amount in data.values():
        total_amount += amount

    return render(request, 'spent/history_categories.html', {'data': data,
                                                             'total_amount': total_amount,
                                                             'month_selected': month_selected,
                                                             'date': date,
                                                             'mois': mois})

@login_required
def history_outlay_view(request, month_selected, category_name):
    user_outlay_category = UserOutlay.objects.filter(user_name=request.user,
                                                     payment_date__month=month_selected,
                                                     outlay__category__name=category_name)
    total_amount = 0
    for amount in user_outlay_category:
        total_amount += amount.amount
    return render(request, 'spent/history_outlay.html', {'user_outlay_category': user_outlay_category,
                                                         'name_category': user_outlay_category[0],
                                                         'month_selected': month_selected,
                                                         'total_amount': total_amount})


@login_required
def outlay_modification_view(request, outlay_id):
    """Outlay modification by user view"""
    outlay_selected = UserOutlay.objects.get(id=outlay_id)
    form = UpdateOutlayForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            payment_date = form.cleaned_data['payment_date']
            UserOutlay.objects.filter(id=outlay_id).update(amount=amount,
                                                           payment_method=payment_method,
                                                           payment_date=payment_date)
            outlay_selected = UserOutlay.objects.get(id=outlay_id)
            success_message = "Modifications prises en compte."
            return render(request, 'spent/outlay_modification.html', {'outlay_selected': outlay_selected,
                                                                      'form': form,
                                                                      'success_message': success_message})

    else:  # if no user's modification
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
    """Delete an user outlay view"""
    outlay_selected = UserOutlay.objects.get(id=outlay_id)
    if request.method == 'POST':
        button_selected = request.POST.get('button_selected')
        if button_selected == "1":  # if the user confirm the suppression
            UserOutlay.objects.filter(id=outlay_id).delete()
            delete = True
            return render(request, 'spent/deleted_outlay.html', {'delete': delete})
    else:
        return render(request, 'spent/deleted_outlay.html', {'outlay_selected': outlay_selected})


@login_required
def empty_useroutlay_view(request):
    """if the user hasn't recorded any outlay"""
    return render(request, 'spent/empty_useroutlay.html')


def expenses_graph_view(request):
    useroutlay = UserOutlay.objects.filter(user_name=request.user)
    if useroutlay.exists() is False:
        return redirect('spent:empty_useroutlay')
    else:
        date = datetime.datetime.now()
        mois = {'01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril', '05': 'Mai', '06': 'Juin',
                '07': 'Juillet', '08': 'Août', '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

        month_selected = request.GET.get('month_list')
        if month_selected:
            user_outlaymonth = UserOutlay.objects.filter(user_name=request.user,
                                                         payment_date__month=month_selected)
            if len(user_outlaymonth) != 0:
                return redirect('spent:expenses_graph_month', month_selected)

            else:
                error_message = ("Aucune dépense enregistrée pour le mois suivant : " + mois[
                    month_selected] + ", renouvellez votre choix.")

                return render(request, 'spent/expenses_graph.html', {'outlay': useroutlay,
                                                              'mois': mois,
                                                              'date': date,
                                                              'error_message': error_message})

    return render(request, 'spent/expenses_graph.html', {'outlay': useroutlay,
                                                  'date': date,
                                                  'mois': mois})


@login_required
def expenses_graph_month_view(request, month_selected):
    mois = {'01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril', '05': 'Mai', '06': 'Juin',
            '07': 'Juillet', '08': 'Août', '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'}

    mois = mois[month_selected]
    outlay = UserOutlay.objects.filter(user_name=request.user,
                                       payment_date__month=month_selected).distinct("outlay__category")

    data = {}
    for categories in outlay:
        categories_amount = UserOutlay.objects.filter(user_name=request.user,
                                                      outlay__category__name=categories.outlay.category.name) \
            .aggregate(category_amount=Sum('amount'))
        data[categories.outlay.category.name] = categories_amount['category_amount']
    print(data)
    return render(request, 'spent/expenses_graph_month.html', {'outlay': outlay,
                                                               'data': data})
