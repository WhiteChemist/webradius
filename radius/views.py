from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.

def index(request):
    return TemplateResponse(request=request,template="templates/pages/index.html")