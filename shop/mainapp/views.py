from django.shortcuts import render

def shop(request):
    return render(request, 'base.html', {})

def test_v(request):
    return render(request, 'index.html', {})