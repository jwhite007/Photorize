from django.db import models
from django.contrib.auth.models import User

# class PublicAlbumsManager(models.Manager):

#     def get_queryset(self):
#         qs = super(PUblicAlbumsManager, self).get_queryset()
#         qs = qs.filter(public__exact=True)
#         return qs


class Tag(models.Model):
    """docstring for Tag"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s ' % (self.name)


class Photo(models.Model):
    """docstring for Photo"""
    owner = models.ForeignKey(
        User,
        related_name='photos',
        related_query_name='photo',
    )
    height = models.IntegerField(blank=True, null=True, default=0)
    width = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(upload_to='images',
                              height_field='height',
                              width_field='width')
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=150)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    def __unicode__(self):
        return u'%s ' % (self.name)

    def owner_name(self):
        raw_name = "%s %s" % (self.owner.first_name,
                              self.owner.last_name)
        name = raw_name.strip()
        if not name:
            name = self.owner.username
        return name


class Album(models.Model):
    """docstring for Album"""
    name = models.CharField(max_length=50)
    photos = models.ManyToManyField(
        Photo,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        related_name='albums',
        related_query_name='album',
    )
    # public = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s ' % (self.name)
