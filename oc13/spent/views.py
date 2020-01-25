from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RecordOutlayForm
from .models import Category, Outlay
# Create your views here.
def expense_history_view(request):
    """expense_history_view"""
    return render(request, 'spent/expense_history.html')

@login_required
def record_outlay_view(request):
    """e"""
    all_categories = Category.objects.all()
    cat_user_selection = request.GET.get('cat_list')
    outlay_cat_selected = Outlay.objects.filter(category=cat_user_selection)
    print(outlay_cat_selected)
    outlay_user_selection = request.GET.get('outlay_list')
    if outlay_user_selection:
        selected_outlay = Outlay.objects.get(id=outlay_user_selection)
        print(selected_outlay)
        print('on est la')
        if request.method == 'POST':
            form = RecordOutlayForm(request.POST)
            if form.is_valid():
                form.save()
        return render(request, 'spent/record_outlay.html', {'categories': all_categories,
                                                            'outlay': outlay_cat_selected,
                                                            'outlay_selected': selected_outlay
                                                            })
    else:

        return render(request, 'spent/record_outlay.html', {'categories': all_categories,
                                                            'outlay': outlay_cat_selected,
                                                            })

def bills_view(request):
    """e"""
    return render(request, 'spent/bills.html')



