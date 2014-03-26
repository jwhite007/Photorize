from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):

#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     eddress = models.CharField(max_length=30)
#     timestamp = models.DateTimeField(auto_now_add=True, blank=False)

#     def __unicode__(self):
#         return self.first_name
        # return self.last_name
        # return self.eddress
        # return self.timestamp


# class PublicAlbumsManager(models.Manager):

#     def get_queryset(self):
#         qs = super(PUblicAlbumsManager, self).get_queryset()
#         qs = qs.filter(public__exact=True)
#         return qs


class Tag(models.Model):
    """docstring for Tag"""
    name = models.CharField(max_length=50)

    # def __init__(self, name):
    #     super(Tag, self).__init__()
    #     self.name = name
    def __unicode__(self):
        return u'%s ' % (self.name)


class Photo(models.Model):
    """docstring for Photo"""
    owner = models.ForeignKey(
        User,
        related_name='photos',
        related_query_name='photo',
    )
    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=150)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    # def __init__(self, image, caption, tag):
    #     super(Photo, self).__init__()
    #     self.image = image
    #     self.caption = caption
    #     self.modified
    def __unicode__(self):
        return u'%s ' % (self.name)


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

    # def __init__(self, name):
    #     super(Album, self).__init__()
    #     self.name = name
