from django.conf.urls import url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = [
	url(r'^$', views.address, name='address'),
	url(r'^edit/$', views.edit, name='edit'),
	url(r'^results/$', views.results, name='results'),
	url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
]
