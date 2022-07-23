from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.

def index(request):
    return TemplateResponse(request=request,template="templates/index.html")

def page_not_found(request,exception):
    return render(request,'techurls/404-page.html',status=404)