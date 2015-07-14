from django.shortcuts import render


def ejemplo(request):
    return render(request, 'ejemplo.html', locals())