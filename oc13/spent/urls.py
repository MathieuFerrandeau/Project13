from django.urls import path


from . import views

app_name = 'spent'
urlpatterns = [
    path('expense-history/', views.expense_history_view, name='expense_history'),
    path('record-expenses/', views.record_expenses_view, name='record_expenses'),
    path('factures/', views.bills_view, name='bills'),
]