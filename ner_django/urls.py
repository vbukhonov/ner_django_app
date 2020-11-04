from django.urls import path

from ner_django import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_files/', views.process_files, name="process_files")
]
