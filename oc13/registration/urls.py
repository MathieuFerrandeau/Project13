from django.urls import path


from . import views

app_name = 'registration'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account_view, name='account'),
    path('contact-form/', views.emailView, name='contact_form'),
    path('success/', views.successView, name='success'),
]
