from django.shortcuts import render
from .models import Category, Outlay
# Create your views here.
def expense_history_view(request):
    """expense_history_view"""
    return render(request, 'spent/expense_history.html')

def record_outlay_view(request):
    """e"""
    all_categories = Category.objects.all()
    all_outlay = Outlay.objects.all()




    return render(request, 'spent/record_outlay.html', {'categories': all_categories,
                                                        'outlay': all_outlay})

def bills_view(request):
    """e"""
    return render(request, 'spent/bills.html')



