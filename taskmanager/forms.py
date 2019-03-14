from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team, Task, Comments
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from .choices import *
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('title', 'users',)

class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    description = forms.CharField(label="Description",max_length=100, widget=forms.Textarea)
    status = forms.ChoiceField(choices = STATUSES, label="Status", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Task
        fields = ('title', 'description', 'team', 'status', 'assignee',)
    
    # def __init__(self, user, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','description', 'assignee','status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)
