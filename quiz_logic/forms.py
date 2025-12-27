from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question, Answer, Profile

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('teacher', 'Вчитель'),
        ('student', 'Учень'),
    )

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'order')

class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'correct')

class AvatarSelectForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)