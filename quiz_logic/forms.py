from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Викторина, Питання, Відповідь

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('teacher', 'Вчитель'),
        ('student', 'Учень'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Викторина
        fields = ['назва', 'опис']

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Питання
        fields = ['текст', 'порядок']

class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Відповідь
        fields = ['текст', 'правильна']

class AvatarSelectForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
