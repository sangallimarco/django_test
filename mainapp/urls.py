from django.conf.urls import patterns, include, url

urlpatterns = patterns('mainapp',
                       url(r'^index/$', 'views.index'),
                       url(r'^(?P<name_id>\d+)/$', 'views.showid'),

                       url(r'^jperson/$', 'views.json_person'),
                       url(r'^jtag/$', 'views.json_tag'),

					   url(r'^tags/$', 'views.tags'),
					   url(r'^groups/$', 'views.groups'),
					   url(r'^login/$', 'views.log_in'),
					   url(r'^logout/$', 'views.log_out'),

					   url(r'^messages/$', 'views.messages'),
					   url(r'^contacts/$', 'views.contacts'),
					   url(r'^new_message/(?P<sender_id>.*)/$', 'views.new_message'),
					   url(r'^reply_message/(?P<message_id>\d+)/$', 'views.reply_message'),

                       url(r'^profile/$','views.profile'),

                       )
