from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Event, Registration


def home(request):
    return render(request, "events/home.html")


def event_list(request):
    category = request.GET.get('category')

    if category:
        events = Event.objects.filter(category=category)
    else:
        events = Event.objects.all()

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "events/event_list.html", {
        "events": page_obj,
        "page_obj": page_obj
    })


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, "events/event_detail.html", {"event": event})


def register_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        college = request.POST.get("college")

        Registration.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone,
            college=college
        )

        return redirect("success")

    return render(request, "events/register.html", {"event": event})


@login_required
def my_registrations(request):
    registrations = Registration.objects.all()
    return render(request, "events/my_registrations.html", {"registrations": registrations})


def cancel_registration(request, id):
    registration = get_object_or_404(Registration, id=id)
    registration.delete()
    return redirect("my_registrations")


def success(request):
    return render(request, "events/success.html")


def dashboard(request):
    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()

    categories = Event.objects.values('category').annotate(total=Count('id'))

    return render(request, "events/dashboard.html", {
        "total_events": total_events,
        "total_registrations": total_registrations,
        "categories": categories
    })