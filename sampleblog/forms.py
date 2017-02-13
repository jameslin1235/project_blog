from django import forms
from .models import Post, Comment, Profile,Category
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class Draft_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text',)


class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)


class Register_form(forms.ModelForm):
    # help_text=password_validation.password_validators_help_text_html()
    password = forms.CharField(widget=forms.PasswordInput,)
    class Meta:
        model = User
        fields = ('username','email','password')

    def clean_password(self):
        data = self.cleaned_data['password']
        if password_validation.validate_password(data) is None:
            return data


class Comment_form(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = Comment
        fields = ('text',)


class Profile_form(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name','last_name','text','avatar')
