from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Person, Request
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
            value = getattr(person, field.name)
            if type(value) == datetime.date:
                formatting = settings.DATE_FORMAT.replace('N', '%B').replace('j', '%d').replace('Y', '%Y')
                birth = value.strftime(formatting).split()
                birth[1] = birth[1].lstrip('0')
                self.assertContains(response, ' '.join(birth))
                pass
            elif field.name != 'id':
                self.assertContains(response, value)


class RequestListViewTest(TestCase):
    def setUp(self):
        middleware_path = 'contact.middleware.RequestSaveMiddleware'
        if middleware_path not in settings.MIDDLEWARE_CLASSES:
            print "NOTE: Ur %s is unplugged" % middleware_path
            settings.MIDDLEWARE_CLASSES = (middleware_path,) + settings.MIDDLEWARE_CLASSES

    def test_requests_saved(self):
        requests = Request.objects.order_by('id')

        for i in range(10):
            self.client.get(reverse('contact:home'), {'q': 'some search param'})
        response = self.client.get(reverse('contact:requests'))
        self.assertEqual(response.status_code, 200)
        if not requests:
            self.fail()
        self.assertQuerysetEqual(response.context['first_req_list'], map(repr, requests[:10]))

    def test_info_presented(self):
        for i in range(10):
            self.client.get(reverse('contact:home'), {'q': 'some search param'})
        response = self.client.get(reverse('contact:requests'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count('Request method'), 10)

        for request in Request.objects.order_by('id')[:10]:
            for field in request._meta.fields:
                value = getattr(request, field.name)
                self.assertContains(response, value)
