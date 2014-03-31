from django.contrib import admin
from django.core.urlresolvers import reverse
from photorizer.models import Photo, Album, Tag


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner_link', 'created', 'modified',
                    )

    def owner_link(self, photo):
        url = reverse('admin:auth_user_change', args=(photo.owner.id,))
        name = photo.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = "Owner"


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner_link', 'created', 'modified',
                    )

    def owner_link(self, album):
        url = reverse('admin:auth_user_change', args=(album.owner.id,))
        name = album.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = "Owner"


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag)
