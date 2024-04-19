from django.shortcuts import render

# -1 Import http response object
from django.http import HttpResponse

# Create your views here.


# -2 Create your function, that returns an http response
def index(request):
    return HttpResponse("This works!")
