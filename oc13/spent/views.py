from django.shortcuts import render

# Create your views here.
def expense_history_view(request):
    """expense_history_view"""
    return render(request, 'spent/expense_history.html')

def record_expenses_view(request):
    """e"""
    return render(request, 'spent/record_expenses.html')

def bills_view(request):
    """e"""
    return render(request, 'spent/bills.html')