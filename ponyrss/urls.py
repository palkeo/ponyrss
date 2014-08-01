from django.conf.urls import patterns, url

urlpatterns = patterns('ponyrss.views',
    url(r'^$', 'home', name='ponyrss-home'),
    url(r'^read/(?P<pk>\d+)/$', 'read', name='ponyrss-read'),

    # Feed management
    url(r'^feeds/$', 'feeds', name='ponyrss-feeds'),
    url(r'^feeds/add/$', 'feed_add', name='ponyrss-feed_add'),
    url(r'^feeds/(?P<pk>\d+)/$', 'feed_edit', name='ponyrss-feed_edit'),
    url(r'^feeds/(?P<pk>\d+)/delete/$', 'feed_delete', name='ponyrss-feed_delete'),
    url(r'^feeds/(?P<pk>\d+)/flush/$', 'feed_flush', name='ponyrss-feed_flush'),
    url(r'^feeds/(?P<pk>\d+)/read/$', 'feed_read', name='ponyrss-feed_read'),
    url(r'^feeds/(?P<pk>\d+)/entries/$', 'feed_entries', name='ponyrss-feed_entries'),
)
