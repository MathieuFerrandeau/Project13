from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail, BadHeaderError
from .forms import RegisterForm, ConnexionForm, AccountUpdateForm, ContactForm


# Create your views here.


def register_view(request):
    """register view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():  # pragma: no cover
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            login(request, account)
            return redirect('core:index')

    else:
        form = RegisterForm()

    help_message = "Votre mot de passe doit contenir au moins 5 caractères dont des lettres."
    return render(request, 'registration/register.html', {'form': form,
                                                          'help_message': help_message})


def logout_view(request):
    logout(request)
    return redirect('core:index')


def login_view(request):
    error = False
    user = request.user
    if user.is_authenticated:
        return redirect('core:index')
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # check if data is correct
            if user:  # if the returned object is not None
                login(request, user)  # connect the user
                return render(request, 'core/index.html')
            else:  # otherwise an error will be displayed
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'registration/login.html', locals())


@login_required()
def account_view(request):
    context = {}

    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['user_form'] = form
    return render(request, 'registration/account.html', context)


def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['assistance.oc13@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('registration:success')
    return render(request, "registration/contact_form.html", {'form': form})


def successView(request):
    return render(request, 'registration/success.html')



