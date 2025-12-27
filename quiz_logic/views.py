from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm
from .models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, Profile
from .forms import UserRegisterForm, QuizCreateForm, QuestionCreateForm, AnswerCreateForm, AvatarSelectForm
from django import forms
from django.contrib.auth.decorators import login_required


# -------------------------
# РЕЄСТРАЦІЯ КОРИСТУВАЧА
# -------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # створюємо користувача та перевіряємо
            user.save()
            role = form.cleaned_data['role']

            # Створюємо профіль тільки якщо його ще немає
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': role})

            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# -------------------------
# ГОЛОВНА
# -------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------
# 1. Список вікторин
# -------------------------
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_logic/quiz_list.html', {
        'quizzes': quizzes
    })


# -------------------------
# 2. Детальна сторінка вікторини
# -------------------------
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_logic/quiz_detail.html', {
        'quiz': quiz
    })


# -------------------------
# 3. Старт вікторини
# -------------------------
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # стартовий екран, без логіки гри
    return render(request, 'quiz_logic/quiz_start.html', {
        'quiz': quiz
    })


# -------------------------
# 4. ПИТАННЯ КВЕСТУ
# -------------------------
def quiz_question(request, quiz_id, question_order):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # отримуємо питання по порядку
    question = get_object_or_404(
        Question,
        quiz=quiz,
        order=question_order
    )

    answers = question.відповіді.all()

    # None — ще не відповіли
    is_correct = None

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer_id')
        selected_answer = get_object_or_404(
            Answer,
            id=selected_answer_id
        )

        # перевірка відповіді
        if selected_answer.правильна:
            is_correct = True
        else:
            is_correct = False

        # перевіряємо, чи є наступне питання
        next_exists = Question.objects.filter(
            quiz=quiz,
            order=question_order + 1
        ).exists()

        # якщо наступного питання немає — фінал
        if not next_exists:
            return redirect('quiz_finish', quiz.id)

    return render(request, 'quiz_logic/quiz_questions.html', {
        'quiz': quiz,
        'question': question,
        'answers': answers,
        'is_correct': is_correct,
        'next_question': question_order + 1
    })


# -------------------------
# 5. ФІНАЛ КВЕСТУ
# -------------------------
def quiz_finish(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, 'quiz_logic/quiz_finish.html', {
        'quiz': quiz
    })


# СТВОРЕННЯ ВІКТОРИНИ (ТІЛЬКИ ДЛЯ ВЧИТЕЛЯ)
@login_required
def create_quiz(request):
    # перевірка ролі
    if request.user.profile.role != 'teacher':
        return redirect('home')

    if request.method == 'POST':
        quiz_form = QuizCreateForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('add_question', quiz.id)
    else:
        quiz_form = QuizCreateForm()

    return render(request, 'quiz_logic/create_quiz.html', {
        'quiz_form': quiz_form
    })


# ДОДАВАННЯ ПИТАННЯ ДО ВІКТОРИНИ
@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.user != quiz.author:
        return redirect('home')

    if request.method == 'POST':
        question_form = QuestionCreateForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_answers', quiz.id, question.id)
    else:
        question_form = QuestionCreateForm()

    return render(request, 'quiz_logic/add_question.html', {
        'quiz': quiz,
        'question_form': question_form
    })


# ДОДАВАННЯ ВІДПОВІДЕЙ
@login_required
def add_answers(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        answer_form = AnswerCreateForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()

            # якщо натиснули "додати ще"
            if 'add_more' in request.POST:
                return redirect('add_answers', quiz.id, question.id)

            # інакше — нове питання
            return redirect('add_question', quiz.id)
    else:
        answer_form = AnswerCreateForm(request.POST or None)

    return render(request, 'quiz_logic/add_answer.html', {
        'quiz': quiz,
        'question': question,
        'answer_form': answer_form
    })


@login_required
def choose_avatar(request):
    # Отримуємо профіль або створюємо, якщо його немає
    profile, created = Profile.objects.get_or_create(user=request.user)

    # визначаємо доступні аватари по ролі
    if profile.role == 'teacher':
        choices = Profile.AVATAR_CHOICES_TEACHER
    else:
        choices = Profile.AVATAR_CHOICES_STUDENT

    if request.method == 'POST':
        form = AvatarSelectForm(request.POST, instance=profile)
        form.fields['avatar'].widget = forms.Select(choices=choices)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AvatarSelectForm(instance=profile)
        form.fields['avatar'].widget = forms.Select(choices=choices)

    # Вказуємо правильний шлях до шаблону
    return render(request, 'quiz_logic/choose_avatar.html', {
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']

            user.profile.role = role
            user.profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')
