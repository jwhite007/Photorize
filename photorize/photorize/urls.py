from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'photorize.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^photos/$', photorizer.views.photos, name='photos'),
    url(r'^photorizer/', include('photorizer.urls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Copied over from Library app.
# urlpatterns = patterns('',
#     url(r'^$', 'main.views.index', name='index'),
#     url(r'^main/', include('main.urls', namespace="main")),
#     url(r'^users/', include('users.urls', namespace="users")),
#     url(r'^books/', include('books.urls', namespace="books")),
#     url(r'^admin/', include(admin.site.urls)),
