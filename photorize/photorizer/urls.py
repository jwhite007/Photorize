from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from photorizer import views
from forms import LoginForm

urlpatterns = patterns('photorizer.views',  # prefix allows you to refer to views by the simple function name.
                       url(r'^photo/(\d+)/$', 'photo_view'),
                       url(r'^main/$', 'main_view', name='homepage'),
                       url(r'^album/(\d+)/$', 'album_view'),
                       url(r'^album/$', 'create_album_view'),
                       url(r'^album/(\d+)/delete/$', 'delete_album_view', name='delete_album'),
                       url(r'^photos/', 'photos_view', name='all_photos'),
                       url(r'^photo/(\d+)/delete/$', 'delete_photo_view', name='delete_photo'),
                       url(r'^AddToAlbum/(\d+)/$', 'add_photo_to_album_view', name='add_to_album'),
                       url(r'^RemoveFromAlbum/(\d+)/$', 'remove_photo_from_album_view', name='remove_from_album'),
                       url(r'^addTag/$', 'add_tag_view', name='add_tag'),
                       # url(r'^(\w+)album/(\d+)$', 'album_view'),
                       # url(r'^profile/(\d+)/$', 'profile'),
                       # url(r'^accounts/register/$', 'register', name='register'),
                       # url(r'^login/$', 'login_view', name='login'),
                       # url(r'^logout/$', 'logout_view', name='logout'),
                       # url(r'^$', 'stub.view', name='app_index'),
                       # url(r'^$', 'stub_view', name="list_photos"),
                       # # can also use: r'^s/(?P<post_id>\d+)/$'
                       # url(r'^photos/(\d+)/$', 'stub_view', name="view_album"),
                       url(r'^photo/add/$', 'add_photo_view', name="add_photo"),
                       # url(r'^albums/$', 'albums', name="albums"),
                       )
urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login', {'template_name': 'registration/login.html'}, name='login'),
                        url(r'^logout/$', 'logout', {'next_page': 'photorizer.views.main_view'}, name='logout'),
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
