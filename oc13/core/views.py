from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    """index view"""
    template = loader.get_template('core/index.html')
    return HttpResponse(template.render(request=request))