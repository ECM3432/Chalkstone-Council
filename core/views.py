# core/views.py

from django.shortcuts import render

def home(request):
    # Return a response to the homepage
    return render(request, 'core/base.html')
