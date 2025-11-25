from django.contrib import admin
from .models import Викторина, Питання, Відповідь, Результат

admin.site.register(Викторина)
admin.site.register(Питання)
admin.site.register(Відповідь)
admin.site.register(Результат)
