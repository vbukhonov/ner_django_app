from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render


def index(request):
    return render(request, 'ner_django/index.html', {})


def process_files(request):
    return HttpResponse("Success!")
