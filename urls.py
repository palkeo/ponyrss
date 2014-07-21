from django.conf.urls import patterns, url

urlpatterns = patterns('sautadet.views',
    url(r'^$', 'home', name='sautadet-home'),
    url(r'^read/(?P<pk>\d+)/$', 'read', name='sautadet-read'),

    # Feed management
    url(r'^feeds/$', 'feeds', name='sautadet-feeds'),
    url(r'^feeds/add/$', 'feed_add', name='sautadet-feed_add'),
    url(r'^feeds/(?P<pk>\d+)/$', 'feed_edit', name='sautadet-feed_edit'),
    url(r'^feeds/(?P<pk>\d+)/delete/$', 'feed_delete', name='sautadet-feed_delete'),
    url(r'^feeds/(?P<pk>\d+)/flush/$', 'feed_flush', name='sautadet-feed_flush'),
    url(r'^feeds/(?P<pk>\d+)/read/$', 'feed_read', name='sautadet-feed_read'),
    url(r'^feeds/(?P<pk>\d+)/entries/$', 'feed_entries', name='sautadet-feed_entries'),
)
