from django.conf.urls import url
from django.contrib import admin, auth
from django import contrib
from django.contrib.auth import views
from datetime import datetime
from .forms import BootstrapAuthenticationForm
from . import views
admin.autodiscover()

urlpatterns = [
	url(r'^address/$', views.address, name='address'),
	url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit'),
	url(r'^(?P<pk>\d+)/$', views.results, name='results'),
	url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
	url(r'^$', contrib.auth.views.login,
		{
			'template_name': 'app/login.html',
			'authentication_form': BootstrapAuthenticationForm,
			'extra_context':
			{
				'title': 'Log in',
				'year': datetime.now().year,
			}
		},
		name='login'),
	url(r'^logout$',
					contrib.auth.views.logout,
					{
						'next_page': '/propinator',
					},
					name='logout'),
]