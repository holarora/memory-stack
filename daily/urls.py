from django.urls import path

from . import views

urlpatterns = [
    path("", views.EntryListView.as_view(), name="all_entries"),
    # path("create/", views.EntryCreateView.as_view(), name="daily"),
]
