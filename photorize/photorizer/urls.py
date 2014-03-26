from django.conf.urls import patterns, url
from photorizer import views


urlpatterns = patterns('photorizer.views',  # prefix allows you to refer to views by the simple function name.
                       # url(r'^$', 'stub.view', name='app_index'),
                       # url(r'^$', 'stub_view', name="list_photos"),
                       # # can also use: r'^s/(?P<post_id>\d+)/$'
                       # url(r'^photos/(\d+)/$', 'stub_view', name="view_album"),
                       url(r'^photo/add/$', 'stub_view', name="add_post"),
                       url(r'^photos/$', 'photos', name="photos"),
                       url(r'^photo/(\d+)/$', 'photo'),
                       url(r'^albums/$', 'albums', name="albums"),
                       url(r'^main/$', 'main', name='homepage'),
                       url(r'^album/(\d+)/$', 'album'),
                       url(r'^profile/(\d+)/$', 'profile'),
                       # url(r'^profile/(\d+)/album/(\d+)/$', 'album'),
                       # url(r'^profile/(\d+)/photo/(\d+)/$', 'photo'),
                       # url(r'^profile/(\d+)/photos/$', 'photos'),
)


# urlpatterns = patterns('blogapp.views',
#     url(r'^$',
#         'stub_view',
#         name="list_posts"),
#     url(r'^posts/(\d+)/$',
#         'stub_view',
#         name="view_post"),
#     url(r'^posts/add/$',
#         'stub_view',
#         name="add_post"),
# )
