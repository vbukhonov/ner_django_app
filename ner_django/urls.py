from django.urls import path

from ner_django import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_files/', views.process_files, name="process_files"),
    path('clean_mongo_database/', views.clean_mongo_database, name="clean_mongo_database")
]
