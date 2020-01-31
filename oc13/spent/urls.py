from django.urls import path


from . import views
from .models import UserOutlay
from django.views.generic.dates import ArchiveIndexView
from .views import UserOutlayArchiveMonthView

app_name = 'spent'
urlpatterns = [
    path('record-outlay/', views.record_outlay_view, name='record_outlay'),
    path('recorded-outlay/', views.outlay_recorded_view, name='outlay_recorded'),
    path('outlay-deleted/<str:outlay_id>/', views.deleted_outlay_view, name='deleted_outlay'),
    path('outlay-modification/<str:outlay_id>/', views.outlay_modification_view, name='outlay_modification'),
    path('factures/', views.bills_view, name='bills'),
    path('history/', views.history, name='history'),
    path('expense-history/', ArchiveIndexView.as_view(model=UserOutlay, date_field="payment_date"),
         name="useroutlay_archive"),
]