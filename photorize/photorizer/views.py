from django.shortcuts import render_to_response, \
    render, redirect, get_object_or_404, get_list_or_404
# from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from models import Photo, Album, Tag
from forms import CreateAlbumForm, \
    PhotoForm, AddtoAlbumForm, RemoveFromAlbumForm, \
    CreateTagForm, DeleteTagForm, EditPhotoForm


def main_view(request):
    if request.user.is_authenticated():
        user_name = request.user.username
        # try:
        #     albums = (Album.objects.filter(
        #         owner__username=user_name).order_by('name'))
        #     # sorted_albums = albums.order_by('-created')
        # except User.DoesNotExist:
        #     raise Http404

        albums = (Album.objects.filter(
            owner__username=user_name).order_by('name'))

        # albums = get_list_or_404(Album, owner__username=user_name)

        context = {'albums': albums, 'username': user_name}
        return render(request, 'photorizer/albums.html', context)
    else:
        return render(request, 'photorizer/welcome.html')


@login_required
def album_view(request, album_id):
    # try:
    #     album = Album.objects.select_related('photos').get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404
    album = get_object_or_404(Album.objects.select_related('photos'), pk=album_id)
    if album.owner_id == request.user.id:
        context = {'album': album, 'username': request.user.username}
        return render(request, 'photorizer/album.html', context)
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
@permission_required('photorizer.change_album', raise_exception=True)
def edit_album_view(request, album_id):
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404
    album = get_object_or_404(Album, pk=album_id)
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
@permission_required('photorizer.delete_album', raise_exception=True)
def delete_album_view(request, album_id):
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404
    album = get_object_or_404(Album, pk=album_id)
    if album.owner_id == request.user.id:
        album.delete()
        return HttpResponseRedirect('/main')
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
def photos_view(request):
    owner_id = request.user.id
    photos = Photo.objects.filter(owner_id=owner_id)
    return render(request, 'photorizer/all_photos.html', {'photos': photos})


@login_required
def photo_view(request, photo_id):
    # try:
    #     photo = Photo.objects.get(pk=photo_id)
    # except Photo.DoesNotExist:
    #     raise Http404
    photo = get_object_or_404(Photo, pk=photo_id)
    if photo.owner_id == request.user.id:
        back = request.META.get('HTTP_REFERER')
        photo = Photo.objects.get(id=photo_id)
        template = loader.get_template('photorizer/photo.html')
        context = RequestContext(request, {
            'photo': photo, 'back': back,
        })
        body = template.render(context)
        return HttpResponse(body, content_type="text/html")
    else:
        return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.add_photo', raise_exception=True)
def add_photo_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.user, request.FILES, data=request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            for tag in form.cleaned_data['tags']:
                photo.tags.add(tag)
            photo.save()
            if form.cleaned_data['tag']:
                tag = Tag(name=form.cleaned_data['tag'], owner=request.user)
                tag.save()
                photo.tags.add(tag)
                photo.save()
            return HttpResponseRedirect('/photos')
    else:
        form = PhotoForm(current_user=request.user)
    return render(request, 'photorizer/add_photo.html', {'form': form})

# @login_required
# @permission_required('photorizer.add_photo', raise_exception=True)
# def add_photo_view(request):
#     if request.method == 'POST':
#         photo_form = PhotoForm(request.POST, request.FILES)
#         tag_form = CreateTagForm(request.POST)
#         if photo_form.is_valid():
#             photo = photo_form.save(commit=False)
#             photo.owner = request.user
#             photo.save()
#             tag_list = []
#             if tag_form.cleaned_data['name']:
#                 tag_name = tag_form.cleaned_data['name']
#                 tag = Tag(name=tag_name)
#                 tag.save()
#                 tag_list.append(tag)
#             for tag in photo_form.cleaned_data['tags']:
#                 tag_list.append(tag)
#             for tag in tag_list:
#                 photo.tags.add(tag)
#             photo.save()
#             return HttpResponseRedirect('/photos')
#     else:
#         photo_form = PhotoForm()
#         tag_form = CreateTagForm()
#     return render(request, 'photorizer/add_photo.html', {'photo_form': photo_form, 'tag_form': tag_form})


@login_required
@permission_required('photorizer.change_photo', raise_exception=True)
def edit_photo_view(request, photo_id):
    # try:
    #     photo = Photo.objects.get(pk=photo_id)
    # except Photo.DoesNotExist:
    #     raise Http404
    photo = get_object_or_404(Photo, pk=photo_id)
    if photo.owner_id == request.user.id:
        if request.method == 'POST':
            form = EditPhotoForm(request.user, data=request.POST or None, instance=photo)
            if form.is_valid():
                photo = form.save()
                if form.cleaned_data['tag']:
                    tag = Tag(name=form.cleaned_data['tag'])
                    tag.save()
                    photo.tags.add(tag)
                    photo.save()
                else:
                    form.save()
                return redirect('photorizer.views.photo_view', photo.id)
        else:
            form = EditPhotoForm(instance=photo, current_user=request.user)
            context = {'form': form, 'photo': photo}
            # return render(request, 'photorizer/edit_photo.html',
            #               {'form': form, 'photo': photo})
            return render(request, 'photorizer/edit_photo.html',
                          context)
    else:
        return render(request, 'photorizer/permission_denied.html')


# @login_required
# @permission_required('photorizer.change_photo', raise_exception=True)
# def edit_photo_view(request, photo_id):
#     try:
#         photo = Photo.objects.get(pk=photo_id)
#     except Photo.DoesNotExist:
#         raise Http404
#     if photo.owner_id == request.user.id:
#         if request.method == 'POST':
#             edit_photo_form = EditPhotoForm(request.POST or None, instance=photo)
#             tag_form = CreateTagForm(request.POST, empty_permitted=True)
#             if edit_photo_form.is_valid():
#                 photo = edit_photo_form.save(commit=False)
#                 # if tag_form.has_changed():
#                 if tag_form.cleaned_data:
#                 # tag_form.save()
#                     tag_name = tag_form.cleaned_data['name']
#                     tag = Tag(name=tag_name)
#                     tag.save()
#                     photo.tags.add(tag)
#                     photo.save()
#                 else:
#                     photo.save()
#                 return redirect('photorizer.views.photo_view', photo.id)
#         else:
#             edit_photo_form = EditPhotoForm(instance=photo)
#             tag_form = CreateTagForm()
#             # tag_form.empty_permitted = True
#             return render(request, 'photorizer/edit_photo.html',
#                           {'edit_photo_form': edit_photo_form,
#                            'tag_form': tag_form, 'photo': photo})
#     else:
#         return render(request, 'photorizer/permission_denied.html')


@login_required
@permission_required('photorizer.delete_photo', raise_exception=True)
def delete_photo_view(request, photo_id):
    # try:
    #     photo = Photo.objects.get(pk=photo_id)
    # except Photo.DoesNotExist:
    #     raise Http404
    photo = get_object_or_404(Photo, pk=photo_id)
    if photo.owner_id == request.user.id:
        photo.delete()
        return HttpResponseRedirect('/photos')
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
            tag_form = CreateTagForm()
        return render(request, 'photorizer/add_to_album.html',
                      {'form': form, 'tag_form': tag_form, 'photo': photo})
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
def tags_view(request):
    # owner_id = request.user.id
    user = request.user
    # photos = Photos.objects.filter(owner_id=owner_id)
    tags = Tag.objects.filter(photo__owner=user)
    tags_list = list(set(tags))
    # tags = Tag.objects.filter()
    return render(request, 'photorizer/tags_list.html', {'tags': tags_list})


@login_required
def tag_view(request, tag_id):
    owner_id = request.user.id
    tag = Tag.objects.get(pk=tag_id)
    photos = tag.photo_set.filter(owner_id=owner_id)
    return render(request, 'photorizer/tags.html', {'photos': photos})


@login_required
@permission_required('photorizer.add_tag', raise_exception=True)
def add_tag_view(request):
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            tag = Tag(name=tag_name, owner=request.user)
            tag.save()
        return redirect('photorizer.views.photos_view')
    else:
        form = CreateTagForm()
    return render(request, 'photorizer/add_tag.html', {'form': form})


# @login_required
# @permission_required('photorizer.delete_tag', raise_exception=True)
# def delete_tag_view(request):
#     user = request.user
#     if request.method == 'POST':
#         form = DeleteTagForm(request.POST)
#         if form.is_valid():
#             for tag in form.cleaned_data['tags']:
#                 tag.delete()
#         return HttpResponseRedirect('/main')
#     else:
#         form = DeleteTagForm()
#         form.fields['tags'] = forms.ModelChoiceField(Tag.objects.filter(photo__owner=user).distinct(), widget=forms.CheckboxSelectMultiple())
#     return render(request, 'photorizer/delete_tag.html', {'form': form})

@login_required
@permission_required('photorizer.delete_tag', raise_exception=True)
def delete_tag_view(request):
    if request.method == 'POST':
        form = DeleteTagForm(request.user, data=request.POST)
        if form.is_valid():
            for tag in form.cleaned_data['names']:
                tag.delete()
        return HttpResponseRedirect('/main')
    else:
        # tags = (Tag.objects.filter(owner_id=request.user.id).order_by('name'))
        context = {'form': DeleteTagForm(current_user=request.user)}
        return render(request, 'photorizer/delete_tag.html', context)
