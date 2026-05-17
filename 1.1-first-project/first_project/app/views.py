from datetime import datetime
from os import listdir

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }
    context = {
        'pages': pages,
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now()
    current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Показать текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    files = listdir()
    msg = f'Показать содержимое рабочей директории: {files}'
    return HttpResponse(msg)
