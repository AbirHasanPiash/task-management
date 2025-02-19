from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome the task management system")

def contact(request):
    return HttpResponse("This is contact page")

def show_task(request):
    return HttpResponse("This is our task page")

def show_specific_task(request, id):
    print(id)
    print(type(id))
    return HttpResponse(f"This is specific task page {id}")