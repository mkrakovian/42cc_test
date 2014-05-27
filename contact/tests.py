from django.test import TestCase
from django.db.models import get_models
from django.template import Template, Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from models import Person, Request, Log
from StringIO import StringIO
import datetime


class HomeViewTest(TestCase):
    fixtures = ['initial_data']

    def test_presenting_info(self):
        person = get_object_or_404(Person, pk=1)
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)

        # Cycle through all the person's fields to check if their values are present on the page.

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


class EditLinkTagTest(TestCase):
    fixtures = ['initial_data']

    def test_tag_works(self):
        person = get_object_or_404(Person, pk=1)
        page = """
        <html>
        {% load edit_extras %}
        {% edit_link person %}
        </html>"""
        t = Template(page)
        c = Context({'person': person})
        response = HttpResponse(t.render(c))
        app = person._meta.app_label
        model = person._meta.model_name

        self.assertContains(response, reverse("admin:%s_%s_change" % (app, model), args=(person.pk,)))


class CountModelObjectsCommandTest(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def test_command(self):
        call_command('count_model_objects', stdout=self.out, stderr=self.err)
        for model in get_models(include_auto_created=True):
            self.out.seek(0)
            self.assertIn(model._meta.model_name.capitalize(), self.out.read())
            self.out.seek(0)
            self.assertIn(str(model._default_manager.count()), self.out.read())


class InsertLogSignalTest(TestCase):
    def setUp(self):
        self.p = Person.objects.create(
            name='Test name',
            surname="Surname",
            birth=timezone.now(),
            bio="Bio",
            email="test@gmail.com",
            skype="test",
            jabber="test@42cc.co",
            contacts="test"
        )

    def test_log_created_action(self):
        log = Log.objects.get(pk=1)
        self.assertEqual(len(Log.objects.all()), 1)
        self.assertEqual(log.action, 'created')

    def test_log_changed_action(self):
        self.p.bio = 'new'
        self.p.save()
        log = Log.objects.get(pk=2)
        self.assertEqual(len(Log.objects.all()), 2)
        self.assertEqual(log.action, 'changed')

    def test_log_deleted_action(self):
        self.p.delete()
        log = Log.objects.get(pk=2)
        self.assertEqual(len(Log.objects.all()), 2)
        self.assertEqual(log.action, 'deleted')


class AuthTest(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.p = Person.objects.get(pk=1)

    def test_not_auth_user(self):
        response = self.client.get(reverse('contact:edit', args=(self.p.id,)))
        self.assertEqual(response.status_code, 302)

    def test_auth_user(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact:edit', args=(self.p.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Save changes')