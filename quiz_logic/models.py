from django.db import models
from django.contrib.auth.models import User


class Викторина(models.Model):
    назва = models.CharField(max_length=255)
    опис = models.TextField(blank=True, null=True)
    створив = models.ForeignKey(User, on_delete=models.CASCADE)
    дата_створення = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.назва


class Питання(models.Model):
    вікторина = models.ForeignKey(Викторина, related_name="питання", on_delete=models.CASCADE)
    текст = models.TextField()
    порядок = models.IntegerField(default=0)

    def __str__(self):
        return f"Питання №{self.порядок}: {self.текст[:40]}"


class Відповідь(models.Model):
    питання = models.ForeignKey(Питання, related_name="відповіді", on_delete=models.CASCADE)
    текст = models.CharField(max_length=255)
    правильна = models.BooleanField(default=False)

    def __str__(self):
        return self.текст


class Результат(models.Model):
    користувач = models.ForeignKey(User, on_delete=models.CASCADE)
    вікторина = models.ForeignKey(Викторина, on_delete=models.CASCADE)
    бали = models.IntegerField(default=0)
    дата = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.користувач.username} — {self.вікторина.назва} — {self.бали}"
