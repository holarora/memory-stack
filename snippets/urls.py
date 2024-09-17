from django.urls import path
from . import views

urlpatterns = [
    path("", views.alltasks, name="alltasks"),
    path("<slug:slug>", views.onetask, name="onetask"),
    path("<slug:slug>/edit/", views.edit_task, name="edit_task"),
]
