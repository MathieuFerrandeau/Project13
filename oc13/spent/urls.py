from django.urls import path


from . import views


app_name = 'spent'
urlpatterns = [
    path('record-outlay/', views.record_outlay_view,
         name='record_outlay'),
    path('recorded-outlay/', views.outlay_recorded_view,
         name='outlay_recorded'),
    path('outlay-deleted/<str:outlay_id>/', views.deleted_outlay_view,
         name='deleted_outlay'),
    path('outlay-modification/<str:outlay_id>/', views.outlay_modification_view,
         name='outlay_modification'),
    path('history/', views.history,
         name='history'),
    path('history/categories/<str:month_selected>/', views.history_categories_view,
         name='history_categories'),
    path('history/outlay/<str:month_selected>/<str:category_name>/', views.history_outlay_view,
         name='history_outlay'),
    path('empty-outlay/', views.empty_useroutlay_view,
         name="empty_useroutlay"),
    path('expenses-graph/', views.expenses_graph_view,
         name="expenses_graph"),
]
