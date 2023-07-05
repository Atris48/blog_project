from django.shortcuts import render

def home(request):
    return render(request, 'home_app/index.html')

def sidebar(request):
    return render(request, 'includes/sidebar.html')