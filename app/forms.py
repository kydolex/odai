from django import forms
from django.db.models import fields
from accounts.models import CustomUser
from django.forms import ModelForm, CharField, TextInput
from .models import Post,Odai,Title
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from . import models

class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    content = forms.CharField(min_length=0, max_length=600,label='小ネタ', widget=forms.Textarea())

class AddOdaiForm(forms.Form):
    title = forms.ModelChoiceField(
        models.Title.objects,
        label='小ネタカテゴリー',
        required=True,
        widget=forms.widgets.Select
    )
    odai = forms.CharField(min_length=0, max_length=600,label='内容', widget=forms.Textarea(attrs={'cols': '20', 'rows': '4'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
