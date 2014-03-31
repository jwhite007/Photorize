from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from models import Photo, Album, Tag
from django.contrib.admin.sites import AdminSite

# new TestCase
class PhotoAdminTestCase(TestCase):
    fixtures = ['some_initial_data.json', ]

    def setUp(self):
        admin = AdminSite()
        self.ma = PostAdmin(Post, admin)
        for author in User.objects.all():
            title = "%s's title" % author.username
            post = Post(title=title, author=author)
            post.save()