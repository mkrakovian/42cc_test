from contact.models import Person
from django.shortcuts import render, get_object_or_404


def home(request):
    person = get_object_or_404(Person, pk=1)
    return render(request, 'contact/home.html', {'person': person})