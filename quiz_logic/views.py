from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .forms import UserRegisterForm

# -------------------------
# РЕЄСТРАЦІЯ КОРИСТУВАЧА
# -------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # створюємо користувача
            user = form.save(commit=False)
            user.save()

            # отримуємо роль з форми
            role = form.cleaned_data['role']

            # створюємо або оновлюємо профіль
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            return redirect('home')  # тут можеш змінити на login або іншу сторінку
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

# -------------------------
# ГОЛОВНА
# -------------------------
def home(request):
    return render(request, 'home.html')
