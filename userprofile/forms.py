from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile

class ProfileRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ProfileRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class ProfileLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ProfileLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].initial = kwargs['instance'].bio

    class Meta:
        model = Profile
        fields = (
            'bio',
        )
