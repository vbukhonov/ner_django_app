from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render


def index(request):
    return render(request, 'ner_django/index.html', {})


def process_files(request):
    return HttpResponse("Success!")


def clean_mongo_database(request):
    return HttpResponse("MongoDB is cleaned.")
