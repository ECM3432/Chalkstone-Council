# comments/views.py
from django.shortcuts import render

# Define the 'home' view
def home(request):
    # You can return a simple response or render a template
    return render(request, 'comments/base.html')  # Replace with your actual template
