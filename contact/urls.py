from django.conf.urls import patterns, url
from django.views.generic import ListView
from contact.models import Request
from contact import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^person/$', ListView.as_view(queryset=Request.objects.order_by('id')[:10],
                                                          context_object_name='first_req_list',
                                                          template_name='contact/requests.html'), name='requests')
                       )
