from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from photorizer import views
from forms import LoginForm

urlpatterns = patterns('photorizer.views',  # prefix allows you to refer to views by the simple function name.
                       url(r'^photo/(\d+)/$', 'photo_view'),
                       url(r'^main/$', 'main_view', name='homepage'),
                       url(r'^album/(\d+)/$', 'album_view'),
                       url(r'^album/$', 'create_album_view'),
                       url(r'^album/(\d+)/delete/$',
                           'delete_album_view', name='delete_album'),
                       url(r'^photos/', 'photos_view', name='all_photos'),
                       url(r'^photo/(\d+)/delete/$',
                           'delete_photo_view', name='delete_photo'),
                       url(r'^album/(\d+)/add_photo$',
                           'add_photo_to_album_view', name='add_to_album'),
                       url(r'^RemoveFromAlbum/(\d+)/$',
                           'remove_photo_from_album_view',
                           name='remove_from_album'),
                       url(r'^addTag/$', 'add_tag_view', name='add_tag'),
                       url(r'^album/(\d+)/edit/$',
                           'edit_album_view', name='edit_album'),
                       url(r'^deleteTag/$',
                           'delete_tag_view', name='delete_tag'),
                       url(r'^photo/(\d+)/edit/$',
                           'edit_photo_view', name='edit_photo'),
                       url(r'^photo/add/$', 'add_photo_view', name="add_photo"),
                       url(r'^tags/$', 'tags_view', name="tags"),
                       url(r'^tag/(\d+)/$', 'tag_view', name='tag'),
                       )
urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login', {'template_name':
                            'registration/login.html'}, name='login'),
                        url(r'^logout/$', 'logout', {'next_page':
                            'photorizer.views.main_view'}, name='logout'),
                        )
