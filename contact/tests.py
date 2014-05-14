from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Person


class HomeViewTest(TestCase):
    fixtures = ['initial_data']

    def test_presenting_info(self):
        person = get_object_or_404(Person, pk=1)
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)

        # Cycle through all the person's fields to check if their values are present on the page.
        # TODO: using the protected _meta, need to find another solution perhaps.

        for field in person._meta.fields:
            if field.name != 'id':
                self.assertContains(response, person.__getattribute__(field.name))