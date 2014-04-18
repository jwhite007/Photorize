from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from models import Photo, Album, Tag


class UserTest(TestCase):
    def setUp(self):
        self.user = User(username='sholmes', email='sholmes@gmail.com',
                         first_name='Sherlock', last_name="Holmes",
                         password='watson')
        self.user.full_clean()
        self.user.save()

    def test_id_creation(self):
        self.assertIsNotNone(self.user.id)

    def test_username_entry(self):
        self.assertEqual(self.user.username, 'sholmes')

    def test_email_entry(self):
        self.assertEqual(self.user.email, 'sholmes@gmail.com')

    def test_first_name_entry(self):
        self.assertEqual(self.user.first_name, 'Sherlock')

    def test_last_name_entry(self):
        self.assertEqual(self.user.last_name, 'Holmes')


class PhotoTest(TestCase):
    def setUp(self):
        self.user = User(username='sholmes', email='sholmes@gmail.com',
                         first_name='Sherlock', last_name="Holmes",
                         password='watson')
        self.user.full_clean()
        self.user.save()
        self.photo = Photo(owner=self.user,
                           image='images/test.png',
                           name='Bocci Ball Reflection',
                           caption='Photo taken in Prague, CZ.')
        self.photo.clean()
        self.photo.save()
        self.tag = Tag(name='Travel')
        self.tag.clean()
        self.tag.save()
        self.photo.tags.add(self.tag)

    def test_id_creation(self):
        self.assertIsNotNone(self.photo.id)

    def test_owner_entry(self):
        self.assertEqual(self.photo.owner.username, 'sholmes')

    def test_image_entry(self):
        self.assertEqual(self.photo.image, 'images/test.png')

    def test_name_entry(self):
        self.assertEqual(self.photo.name, 'Bocci Ball Reflection')

    def test_caption_entry(self):
        self.assertEqual(self.photo.caption, 'Photo taken in Prague, CZ.')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Travel')

    def test_photo_tag_association(self):
        tags = Tag.objects.filter(photo=self.photo.id)
        self.assertEqual(tags[0].name, 'Travel')


class AlbumTest(TestCase):
    def setUp(self):
        self.user = User(username='sholmes', email='sholmes@gmail.com',
                         first_name='Sherlock', last_name="Holmes",
                         password='watson')
        self.user.full_clean()
        self.user.save()
        self.photo = Photo(owner=self.user,
                           image='images/test.png',
                           name='Bocci Ball Reflection',
                           caption='Photo taken in Prague, CZ.')
        self.photo.clean()
        self.photo.save()
        self.tag = Tag(name='Travel')
        self.tag.clean()
        self.tag.save()
        self.photo.tags.add(self.tag)
        self.album = Album(owner=self.user,
                           name='Czech Republic')
        self.album.clean()
        self.album.save()
        self.album.photos.add(self.photo)

    def test_id_creation(self):
        self.assertIsNotNone(self.album.id)

    def test_owner_entry(self):
        self.assertEqual(self.album.name, 'Czech Republic')

    def test_name_entry(self):
        self.assertEqual(self.photo.name, 'Bocci Ball Reflection')

    def test_album_to_photo_association(self):
        photos = Photo.objects.filter(album=self.album.id)
        self.assertEqual(photos[0].name, 'Bocci Ball Reflection')
