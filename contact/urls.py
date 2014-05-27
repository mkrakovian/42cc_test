from django.conf.urls import patterns, url
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from contact.models import Request
from contact import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^requests/$', ListView.as_view(queryset=Request.objects.order_by('id')[:10],
                                                          context_object_name='first_req_list',
                                                          template_name='contact/requests.html'), name='requests'),
                       url(r'^edit/(?P<pk>\d+)/$', login_required(views.UpdatePersonView.as_view()), name='edit'),
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', views.logout_view, name='logout')
                       )
