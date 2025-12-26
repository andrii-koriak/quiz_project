from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Вчитель'),
        ('student', 'Учень'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    made = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Питання(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="питання", on_delete=models.CASCADE)
    text = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Питання №{self.order}: {self.text[:40]}"


class Answer(models.Model):
    question = models.ForeignKey(Питання, related_name="відповіді", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    rog = models.BooleanField(default=False)

    def __str__(self):
        return self.текст


class Результат(models.Model):
    користувач = models.ForeignKey(User, on_delete=models.CASCADE)
    вікторина = models.ForeignKey(Викторина, on_delete=models.CASCADE)
    бали = models.IntegerField(default=0)
    дата = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.користувач.username} — {self.вікторина.назва} — {self.бали}"
