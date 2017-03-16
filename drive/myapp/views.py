from django.shortcuts import render
from .models import *


def show_genres(request):
    return render(request, 'myapp/genres.html', {'nodes':Genre.objects.all()})