from django.conf.urls import patterns, url

from repolab import views

urlpatterns = patterns('',
    url(r'^$', views.Homepage.as_view(), name='homepage_url'),
    url(r'^changeset/(?P<changeset>[\w\d]+)/$', views.ViewChangeset.as_view(), name='revision_url'),
)
