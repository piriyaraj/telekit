from math import floor
from django import forms
from django.forms.forms import Form

from .models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
    


class UserRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username", "email", "password", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username)
        
        if user.exists():
            raise forms.ValidationError("A user with that name already exists")
        
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email)
        
        if user.exists():
            raise forms.ValidationError("A user with that email already exists")
        
        return self.cleaned_data.get('email')


    def clean_password(self):
        password = self.cleaned_data.get('password')
        confim_password = self.data.get('confirm_password')
        
        if password != confim_password:
            raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data.get('password')


class UserProfileUpdateForm(forms.ModelForm):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        
        if user.exists():
            raise forms.ValidationError("A user with that name already exists")
        
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        
        if user.exists():
            raise forms.ValidationError("A user with that email already exists")
        
        return self.cleaned_data.get('email')

    def change_password(self):
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_password = self.data['new_password']
            confirm_password = self.data['confirm_password']
            if new_password != '' and confirm_password != '':
                if new_password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
                else:
                    self.instance.set_password(new_password)
                    self.instance.save()

    def clean(self):
        self.change_password()


class ProfilePictureUpdateForm(forms.Form):
    profile_image = forms.ImageField(required=True)

class Pinlinks(forms.Form):
    max_points = 0
    days = forms.IntegerField(label='Days', initial=1, min_value=1)
    points = forms.FloatField(
        label='Points',
        # decimal_places=2
    )

    def __init__(self, *args, **kwargs):
        max_points = kwargs.pop('max_points', None)
        self.max_points = max_points
        min_points = kwargs.pop('min_points', None)
        super(Pinlinks, self).__init__(*args, **kwargs)
        print(max_points)
        # Set max_value dynamically
        if max_points is not None:
            self.fields['points'].widget.attrs['max'] = max_points
            self.fields['points'].widget.attrs['min'] = min_points
            self.fields['points'].initial = floor(max_points)
        
    # def clean_points(self):
    #     points = self.cleaned_data.get('points')

    #     if points is not None and points <= 0:
    #         raise ValidationError("Points must be greater than 0.")
    #     elif points > self.max_points:
    #         raise ValidationError(f"Points value should be less than {self.max_points}.")

    #     return points