import os

from django.conf import settings
from pymongo import MongoClient

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

from ner_django.utils import process_archive

mongodb = MongoClient(f"{settings.MONGO_DB_URI}/{settings.MONGO_DB_NAME}").get_database()


def index(request):
    return render(request, 'ner_django/index.html', {})


def process_files(request):
    inputs_dir = "./inputs"
    try:
        for name in os.listdir(inputs_dir):
            path = os.path.join(inputs_dir, name)
            if os.path.isfile(path):
                process_archive(path, mongodb)
        return HttpResponse("Success!")
    except Exception as e:
        return HttpResponseServerError("Something went wrong")


def clean_mongo_database(request):
    mongodb.patents.drop()
    return HttpResponse("MongoDB is cleaned.")
