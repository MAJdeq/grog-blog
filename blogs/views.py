from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles import finders
from .forms import CustomLoginForm, CustomRegistrationForm

def index(request):
    return render(request, "home.html", {})

def custom_css(request):
    css_path = finders.find('blogs/style.css')

    if css_path:
        with open(css_path, 'r') as css_file:
            css_content = css_file.read()

        response = HttpResponse(css_content, content_type='text/css')
        return response
    else:
        return HttpResponse(status=404)
