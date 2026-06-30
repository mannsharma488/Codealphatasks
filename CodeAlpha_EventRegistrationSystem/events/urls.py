from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("events/", views.event_list, name="event_list"),
    path("event/<int:id>/", views.event_detail, name="event_detail"),
    path("register/<int:id>/", views.register_event, name="register_event"),
    path("my-registrations/", views.my_registrations, name="my_registrations"),
    path("cancel/<int:id>/", views.cancel_registration, name="cancel_registration"),

    # NEW
    path("success/", views.success, name="success"),
    path("dashboard/", views.dashboard, name="dashboard"),
]