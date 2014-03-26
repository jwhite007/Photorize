from django.shortcuts import render_to_response, \
    render, redirect, get_object_or_404
# from users.forms import UsersForm
# from users.models import users
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Photo, Album
from django.template import RequestContext, loader
from django.contrib.auth.models import User
# Create your views here.


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def main(request):
    msg = 'THIS IS THE MAIN PAGE'
    return render_to_response('photorizer/main.html', {'msg': msg})


def photos(request):
    # print('photos')
    # return HttpResponse('this is a photo test')
    # user1 = User.objects.get(id=user)
    photos = Photo.objects.all().order_by('name')[:]
    return render_to_response('photorizer/photos.html', {'photos': photos})


def photo(request, photo):
    # user1 = User.objects.get(id=user)
    print(photo)
    photo = Photo.objects.get(id=photo)
    print(photo)
    template = loader.get_template('photorizer/photo.html')
    context = RequestContext(request, {
        'photo': photo,
    })
    body = template.render(context)
    return HttpResponse(body, content_type="text/html")

# def upload_photo():
#     pass


def album(request, album):
    print "album is " + album
    # user1 = User.objects.get(id=user)
    # print(user1.username)
    # album = Album.objects.get(id=1)
    print(album)
    # photos = album.photos[:]
    photos = Photo.objects.filter(album=album)
    for photo in photos:
        print(photo)
    template = loader.get_template('photorizer/album.html')
    context = RequestContext(request, {
        'photos': photos,
    })
    body = template.render(context)
    return HttpResponse(body, content_type="text/html")
    # return HttpResponse('this is the albums page', content_type="text/plain")
    #


def albums(request, user):
    print(user)
    albums = Album.objects.filter(user=user.id)
    # body = 'this is an albums page'
    # return HttpResponse(body, content_type="text/plain")
    # albums = Album.objects.all().order_by('name')[:]
    return render_to_response('photorizer/albums.html', {'albums': albums})


def profile(request, user):
    user1 = User.objects.get(id=user)
    albums = Album.objects.filter(owner_id=user)
    photos = Photo.objects.filter(owner_id=user)
    for album in albums:
        albumid = album.id
        albumsphotos = Photo.objects.filter(album=albumid)
        for photo in albumsphotos:
            print(photo.name)
    print(user1.username)
    return render_to_response('photorizer/profile.html',
                              {'user': user1,
                              'albums': albums,
                              'photos': photos})

