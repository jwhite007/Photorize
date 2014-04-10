from django.shortcuts import render_to_response, \
    render, redirect, get_object_or_404
from django.http import Http404
# from users.forms import UsersForm
# from users.models import users
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Photo, Album, Tag
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from forms import LoginForm, CreateAlbumForm, \
    PhotoForm, AddtoAlbumForm, RemoveFromAlbumForm, \
    CreateTagForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms


def main_view(request):
    if request.user.is_authenticated():
        user_name = request.user.username
        print(user_name)
        try:
            albums = (Album.objects.filter(
                owner__username=user_name).order_by('name'))
            # sorted_albums = albums.order_by('-created')
        except User.DoesNotExist:
            raise Http404
        context = {'albums': albums, 'username': user_name}
        return render(request, 'photorizer/albums.html', context)
    else:
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'registration/login.html', context)


@login_required
def photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
    # user1 = User.objects.get(id=user)
        back = request.META.get('HTTP_REFERER')
        photo = Photo.objects.get(id=photo_id)
        template = loader.get_template('photorizer/photo.html')
        context = RequestContext(request, {
            'photo': photo, 'back': back
        })
        body = template.render(context)
        return HttpResponse(body, content_type="text/html")
    else:
        return render(request, 'photorizer/permission_denied.html')

# def upload_photo():
#     pass


@login_required
# @permission_required
def album_view(request, album_id):
    album = Album.objects.select_related('photos').get(pk=album_id)
    print("album owner: " + album.owner.username)
    print("request user: " + request.user.username)
    print("request user id: " + str(request.user.id))
    context = {'album': album}
    if album.owner.username == request.user.username:
        return render(request, 'photorizer/album.html', context)
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
def create_album_view(request):
    user_id = request.user.id
    owner = request.user
    if request.method == 'POST':
        form = CreateAlbumForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            album = Album(name=name, owner=owner)
            album.save()
            return HttpResponseRedirect('/main')
    else:
        form = CreateAlbumForm()
    return render(request, 'photorizer/create_album.html', {'form': form})


def delete_album_view(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    return HttpResponseRedirect('/main')


def delete_photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.delete()
    return HttpResponseRedirect('/photos')


def add_photo_view(request):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        # tag_form = TagForm(request.POST)
        # if tag_form.is_valid():
        #     tag_form.save()
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.owner = request.user
            # photo = Photo()
            # photo.image = form.cleaned_data['image']
            # photo.name = form.cleaned_data['name']
            # photo.caption = form.cleaned_data['caption']
            # photo.tags = form.cleaned_data['tags']
            photo.save()
            for tag in photo_form.cleaned_data['tags']:
                photo.tags.add(tag)
            photo.save()
            return HttpResponseRedirect('/photos')
    else:
        form = PhotoForm()
    return render(request, 'photorizer/add_photo.html', {'form': form})


def add_photo_to_album_view(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(pk=photo_id)
        form = AddtoAlbumForm(request.POST)
        if form.is_valid():
            for album in form.cleaned_data['albums']:
                album.photos.add(photo)
                album.save()
        return HttpResponseRedirect('/main')
    else:
        photo = Photo.objects.get(pk=photo_id)
        form = AddtoAlbumForm()
    return render(request, 'photorizer/add_to_album.html', {'form': form, 'photo': photo})


def remove_photo_from_album_view(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(pk=photo_id)
        form = RemoveFromAlbumForm(request.POST)
        # form.fields['albums'] = forms.ModelChoiceField(Album.objects.filter(photos=photo_id)
        if form.is_valid():
            for album in form.cleaned_data['albums']:
                album.photos.remove(photo)
                album.save()
        return HttpResponseRedirect('/main')
    else:
        photo = Photo.objects.get(pk=photo_id)
        form = RemoveFromAlbumForm()
        form.fields['albums'] = forms.ModelChoiceField(Album.objects.filter(photos=photo_id), widget=forms.CheckboxSelectMultiple())
    return render(request, 'photorizer/remove_from_album.html', {'form': form, 'photo': photo})


def photos_view(request):
    owner_id = request.user.id
    photos = Photo.objects.filter(owner_id=owner_id)
    return render(request, 'photorizer/all_photos.html', {'photos': photos})


def add_tag_view(request):
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            tag = Tag(name=tag_name)
            tag.save()
        return redirect('photorizer.views.add_photo_view')
    else:
        form = CreateTagForm()
    return render(request, 'photorizer/add_tag.html', {'form': form})

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
