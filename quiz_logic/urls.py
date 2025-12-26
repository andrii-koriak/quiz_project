from django.urls import path
from . import views
from . import views as quiz_views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # розлогінює користувача
    return redirect('home')  # переадресація на головну або потрібну сторінку

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/start/', views.quiz_start, name='quiz_start'),
    path('logout/', logout_view, name='logout'),
    # питання квесту
    path('<int:quiz_id>/question/<int:question_order>/', views.quiz_question,name='quiz_question'),
    # фінал
    path('<int:quiz_id>/finish/', views.quiz_finish,name='quiz_finish'),
    # створення вікторин (для вчителя)
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('<int:quiz_id>/question/<int:question_id>/add-answers/', views.add_answers, name='add_answers'),
    path('choose-avatar/', views.choose_avatar, name='choose_avatar'),


]
