from django.conf.urls import patterns, include, url

urlpatterns = patterns('mainapp',
                       url(r'^index/$', 'views.index'),
                       url(r'^(?P<name_id>\d+)/$', 'views.showid'),

                       url(r'^jperson/$', 'views.json_person'),
                       url(r'^jtag/$', 'views.json_tag'),

					   url(r'^tags/$', 'views.tags'),
					   url(r'^groups/$', 'views.groups'),

                       )
