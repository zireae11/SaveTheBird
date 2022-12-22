from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main.forms import LoginForm, RegisterForm
import mimetypes
import os
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper


def home(request):
    return render(request, 'main/home.html')

def downloadfile(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'mysetup.exe'
    filepath = base_dir + '/files/' + filename
    thefile = filepath
    filename = os.path.basename(thefile)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
        content_type = mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename

    return response



# страница пользователя
def me(request):
    # если не авторизован, то редирект на страницу входа
    if not request.user.is_authenticated:

        return redirect('login')
    # рендерим шаблон и передаем туда объект пользователя

    if request.method == "POST":
        new_url = request.POST.get("new_url")
        output = "<h2>{0}</h2>".format(new_url)
        return HttpResponse(output)

    return render(request, 'main/me.html', {'user': request.user})


# выход
def doLogout(request):
    # вызываем функцию django.contrib.auth.logout и делаем редирект на страницу входа
    logout(request)
    return redirect('login')

# страница входа
def loginPage(request):

    # инициализируем объект класса формы
    form = LoginForm()

    # обрабатываем случай отправки формы на этот адрес
    if request.method == 'POST':

        # заполянем объект данными, полученными из запроса
        form = LoginForm(request.POST)

        # проверяем валидность формы
        if form.is_valid():
            # пытаемся авторизовать пользователя
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # если существует пользователь с таким именем и паролем,
                # то сохраняем авторизацию и делаем редирект
                login(request, user)
                return redirect('me')
            else:
                # иначе возвращаем ошибку
                form.add_error(None, 'Неверные данные!')

    # рендерим шаблон и передаем туда объект формы
    return render(request, 'main/login.html', {'form': form})


# регистрация
def registerPage(request):

    # инициализируем объект формы
    form = RegisterForm()

    if request.method == 'POST':
        # заполняем объект данными формы, если она была отправлена
        form = RegisterForm(request.POST)

        if form.is_valid():
            # если форма валидна - создаем нового пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('login')
    # ренедерим шаблон и передаем объект формы
    return render(request, 'main/registration.html', {'form': form})
