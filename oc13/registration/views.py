from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.


def register(request):
    """register view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:index')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

