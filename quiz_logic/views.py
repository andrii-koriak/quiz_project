from django.shortcuts import render, get_object_or_404
from .models import Викторина


# 1. Список вікторин
def quiz_list(request):
    quizzes = Викторина.objects.all()
    return render(request, 'quiz_logic/quiz_list.html', {'quizzes': quizzes})


# 2. Детальна сторінка вікторини
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Викторина, id=quiz_id)
    return render(request, 'quiz_logic/quiz_detail.html', {'quiz': quiz})


# 3. Старт вікторини
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Викторина, id=quiz_id)
    questions = quiz.питання.all()

    return render(request, 'quiz_logic/quiz_start.html', {
        'quiz': quiz,
        'questions': questions
    })
