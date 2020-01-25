from django.urls import path


from . import views

app_name = 'spent'
urlpatterns = [
    path('expense-history/', views.expense_history_view, name='expense_history'),
    path('record-outlay/', views.record_outlay_view, name='record_outlay'),
    path('factures/', views.bills_view, name='bills'),
]