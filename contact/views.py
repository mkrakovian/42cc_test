from contact.models import Person
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth import logout


def home(request):
    person = get_object_or_404(Person, pk=1)
    return render(request, 'contact/home.html', {'person': person})


class UpdatePersonView(UpdateView):
    model = Person
    template_name = 'contact/edit.html'

    def get_success_url(self):
        return reverse('contact:home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('contact:home'))