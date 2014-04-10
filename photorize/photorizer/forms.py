from django import forms
from registration.forms import RegistrationForm
from photorizer.models import Photo, Album, Tag
from django.forms import ModelForm, CharField, ChoiceField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(RegistrationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class CreateAlbumForm(forms.Form):
    name = forms.CharField(max_length=50)


class PhotoForm(ModelForm):
    # name = forms.CharField(max_length=50)
    # tags = forms.ChoiceField()
    # image = forms.imageField()

    class Meta:
        model = Photo
        fields = [
            'image', 'name', 'caption', 'tags']


class CreateTagForm(forms.Form):
    name = forms.CharField(max_length=50)


class AddtoAlbumForm(forms.Form):
    albums = forms.ModelMultipleChoiceField(queryset=Album.objects.all(),
                                            widget=forms.CheckboxSelectMultiple())


class RemoveFromAlbumForm(forms.Form):
    albums = forms.ModelMultipleChoiceField(queryset=Album.objects.all(),
                                            widget=forms.CheckboxSelectMultiple())
