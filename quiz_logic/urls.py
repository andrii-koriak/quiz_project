from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/start/', views.quiz_start, name='quiz_start'),
]


#/quiz_logic/ — список викторин

#/quiz_logic/5/ — детальная страница викторины

#/quiz_logic/5/start/ — старт прохождения