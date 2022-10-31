from django.http import HttpResponse
from urllib3 import HTTPResponse
from django.template.response import TemplateResponse

# Create your views here.

def index(request):
    return TemplateResponse(request,template="templates/index.html")

def adduser(request):
    return TemplateResponse(request,template="templates/adduser_page.html")

def updateuser(request):
    return TemplateResponse(request,template="templates/updateuser_page.html")

def deleteuser(request):
    return TemplateResponse(request,template="templates/deleteuser_page.html")

def addgroup(request):
    return TemplateResponse(request,template="templates/addgroup_page.html")

def updategroup(request):
    return TemplateResponse(request,template="templates/updategroup_page.html")

def deletegroup(request):
    return TemplateResponse(request,template="templates/deletegroup_page.html")

def handler404(request,exception):
    return render(request,template='templates/404.html',status=404)