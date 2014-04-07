from django.shortcuts import render_to_response, \
    render, redirect, get_object_or_404
from django.http import Http404
# from users.forms import UsersForm
# from users.models import users
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Photo, Album
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required


def main_view(request):
    if request.user.is_authenticated():
        user_name = request.user.username
        print(user_name)
        try:
            albums = (Album.objects.filter(
                owner__username=user_name))
            sorted_albums = albums.order_by('-created')
        except User.DoesNotExist:
            raise Http404
        context = {'albums': sorted_albums, 'username': user_name}
        return render(request, 'photorizer/albums.html', context)
    else:
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'registration/login.html', context)


@login_required
def photo_view(request, photo):
    # user1 = User.objects.get(id=user)
    back = request.META.get('HTTP_REFERER')
    photo = Photo.objects.get(id=photo)
    template = loader.get_template('photorizer/photo.html')
    context = RequestContext(request, {
        'photo': photo, 'back': back
    })
    body = template.render(context)
    return HttpResponse(body, content_type="text/html")

# def upload_photo():
#     pass


@login_required
# @permission_required
def album_view(request, album_id):
    album = Album.objects.select_related('photos').get(pk=album_id)
    context = {'album': album}
    return render(request, 'photorizer/album.html', context)


# @login_required
# def album_view(request, owner, album_id):
#     album = Album.objects.select_related('photos').get(pk=album_id)
#     context = {'album': album}
#     return render(request, 'photorizer/album.html', context)
    # user1 = User.objects.get(id=user)
    # print(user1.username)
    # album = Album.objects.get(id=1)
    # photos = album.photos[:]
    # photos = Photo.objects.filter(album=album)
    # for photo in photos:
    #     print(photo)
    #     print(photo.image)
    # template = loader.get_template('photorizer/album.html')
    # context = RequestContext(request, {
    #     'photos': photos, 'album': album
    # })
    # body = template.render(context)
    # return HttpResponse(body, content_type="text/html")
    # return HttpResponse('this is the albums page', content_type="text/plain")


# def albums(request, user):
#     # print(user)
#     # albums = Album.objects.filter(owner_id=user)
#     # body = 'this is an albums page'
#     # return HttpResponse(body, content_type="text/plain")
#     albums = Album.objects.all().order_by('name')[:]
#     return render_to_response('photorizer/albums.html', {'albums': albums})


# def profile(request, user):
#     user1 = User.objects.get(id=user)
#     albums = Album.objects.filter(owner_id=user)
#     photos = Photo.objects.filter(owner_id=user)
#     for album in albums:
#         albumid = album.id
#         albumsphotos = Photo.objects.filter(album=albumid)
#         for photo in albumsphotos:
#             print(photo.name)
#     print(user1.username)
#     return render_to_response('photorizer/profile.html',
#                               {'user': user1,
#                               'albums': albums,
#                               'photos': photos})


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")
