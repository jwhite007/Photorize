from django.shortcuts import render_to_response, \
    render, redirect, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Photo, Album, Tag
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from forms import CreateAlbumForm, \
    PhotoForm, AddtoAlbumForm, RemoveFromAlbumForm, \
    CreateTagForm, DeleteTagForm, EditPhotoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms


# def main_view(request):
#     if request.user.is_authenticated():
#         user_name = request.user.username
#         try:
#             albums = (Album.objects.filter(
#                 owner__username=user_name).order_by('name'))
#             # sorted_albums = albums.order_by('-created')
#         except User.DoesNotExist:
#             raise Http404
#         context = {'albums': albums, 'username': user_name}
#         return render(request, 'photorizer/albums.html', context)
#     else:
#         login_form = LoginForm()
#         context = {'form': login_form}
#         return render(request, 'registration/login.html', context)

@login_required
def main_view(request):
    user_name = request.user.username
    try:
        albums = (Album.objects.filter(
            owner__username=user_name).order_by('name'))
        # sorted_albums = albums.order_by('-created')
    except User.DoesNotExist:
        raise Http404
    context = {'albums': albums, 'username': user_name}
    return render(request, 'photorizer/albums.html', context)


@login_required
def photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
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


@login_required
def album_view(request, album_id):
    album = Album.objects.select_related('photos').get(pk=album_id)
    if album.owner_id == request.user.id:
        print("album owner: " + album.owner.username)
        print("request user: " + request.user.username)
        print("request user id: " + str(request.user.id))
        context = {'album': album}
        if album.owner.username == request.user.username:
            return render(request, 'photorizer/album.html', context)
        else:
            return render(request, 'photorizer/permission_denied.html')
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.add_album', raise_exception=True)
def create_album_view(request):
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


@login_required
@permission_required('photorizer.delete_album', raise_exception=True)
def delete_album_view(request, album_id):
    album = Album.objects.get(pk=album_id)
    if album.owner_id == request.user.id:
        album.delete()
        return HttpResponseRedirect('/main')
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.change_album', raise_exception=True)
def edit_album_view(request, album_id):
    album = Album.objects.get(pk=album_id)
    if album.owner_id == request.user.id:
        if request.method == 'POST':
            form = CreateAlbumForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                album.name = name
                album.save()
                return HttpResponseRedirect('/main')
        else:
            form = CreateAlbumForm(initial={'name': album.name})
        return render(request, 'photorizer/edit_album.html',
                      {'form': form, 'album': album})
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.delete_photo', raise_exception=True)
def delete_photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
        photo.delete()
        return HttpResponseRedirect('/photos')
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.add_photo', raise_exception=True)
def add_photo_view(request):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.owner = request.user
            photo.save()
            for tag in photo_form.cleaned_data['tags']:
                photo.tags.add(tag)
            photo.save()
            return HttpResponseRedirect('/photos')
    else:
        form = PhotoForm()
    return render(request, 'photorizer/add_photo.html', {'form': form})


@login_required
@permission_required('photorizer.change_photo', raise_exception=True)
def edit_photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
        form = EditPhotoForm(request.POST or None, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photorizer.views.photo_view', photo.id)
        return render(request, 'photorizer/edit_photo.html',
                      {'form': form, 'photo': photo})
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.change_album', raise_exception=True)
def add_photo_to_album_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
        if request.method == 'POST':
            form = AddtoAlbumForm(request.POST)
            if form.is_valid():
                for album in form.cleaned_data['albums']:
                    album.photos.add(photo)
                    album.save()
            return HttpResponseRedirect('/main')
        else:
            form = AddtoAlbumForm()
        return render(request, 'photorizer/add_to_album.html',
                      {'form': form, 'photo': photo})
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.change_album', raise_exception=True)
def remove_photo_from_album_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if photo.owner_id == request.user.id:
        if request.method == 'POST':
            form = RemoveFromAlbumForm(request.POST)
            # form.fields['albums'] = forms.ModelChoiceField(Album.objects.filter(photos=photo_id)
            if form.is_valid():
                for album in form.cleaned_data['albums']:
                    album.photos.remove(photo)
                    album.save()
            return HttpResponseRedirect('/main')
        else:
            form = RemoveFromAlbumForm()
            form.fields['albums'] = forms.ModelChoiceField(Album.objects.filter(photos=photo_id), widget=forms.CheckboxSelectMultiple())
        return render(request, 'photorizer/remove_from_album.html',
                      {'form': form, 'photo': photo})
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.delete_tag', raise_exception=True)
def delete_tag_view(request):
    if request.method == 'POST':
        form = DeleteTagForm(request.POST)
        if form.is_valid():
            for tag in form.cleaned_data['tags']:
                tag.delete()
        return HttpResponseRedirect('/main')
    else:
        form = DeleteTagForm()
        # form.fields['tags'] = forms.ModelChoiceField(Tag.objects.all(), widget=forms.CheckboxSelectMultiple())
    return render(request, 'photorizer/delete_tag.html', {'form': form})


@login_required
def photos_view(request):
    owner_id = request.user.id
    photos = Photo.objects.filter(owner_id=owner_id)
    return render(request, 'photorizer/all_photos.html', {'photos': photos})


@login_required
@permission_required('photorizer.add_tag', raise_exception=True)
def add_tag_view(request):
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            tag = Tag(name=tag_name)
            tag.save()
        return redirect('photorizer.views.photos_view')
    else:
        form = CreateTagForm()
    return render(request, 'photorizer/add_tag.html', {'form': form})
