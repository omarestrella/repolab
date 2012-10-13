from django.conf.urls import patterns, url

from repolab import views

urlpatterns = patterns('',
    url(r'^$', views.Homepage.as_view(), name='homepage_url'),

    url(r'^repo/(?P<slug>[\w\d]+)/$', views.ViewRepo.as_view(), name='repo_url'),

    url(r'^repo/(?P<slug>[\w\d]+)/tree/(?P<changeset>[\w\d]+)/$',
        views.ViewChangeset.as_view(), name='repo_changeset_url'),
    url(r'^repo/(?P<slug>[\w\d]+)/tree/(?P<changeset>[\w\d]+)/(?P<path>.*)/$',
        views.ViewChangesetPath.as_view(), name='repo_path_url'),

    url(r'^repo/(?P<slug>[\w\d]+)/edit/(?P<changeset>[\w\d]+)/(?P<path>[.*])/$',
        views.EditChangesetPath.as_view(), name='repo_edit_url'),

    url(r'^repo/(?P<slug>[\w\d]+)/commit/(?P<changeset>[\w\d]+)/(?P<path>[.*])/$',
        views.ViewChangesetCommit.as_view(), name='repo_commit_url'),
)
