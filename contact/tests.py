from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Person
from django.conf import settings
import datetime


class HomeViewTest(TestCase):
    fixtures = ['initial_data']

    def test_presenting_info(self):
        person = get_object_or_404(Person, pk=1)
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)

        # Cycle through all the person's fields to check if their values are present on the page.
        # TODO: using the protected _meta, need to find another solution perhaps.

        for field in person._meta.fields:
            value = person.__getattribute__(field.name)
            if type(value) == datetime.date:
                formatting = settings.DATE_FORMAT.replace('N ', '%B').replace('j', '%e').replace('Y', '%Y')
                self.assertContains(response, value.strftime(formatting))
                pass
            elif field.name != 'id':
                self.assertContains(response, value)