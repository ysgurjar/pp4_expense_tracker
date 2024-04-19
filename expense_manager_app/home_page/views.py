from django.shortcuts import render

# Import http response object
from django.http import HttpResponse

# Import render_to_string object to serve html templates
from django.template.loader import render_to_string

# ===== Create your views here.

# Create your function, that returns an http response
def index(request):
    response=render_to_string("home_page/index.html")
    return HttpResponse(response)
