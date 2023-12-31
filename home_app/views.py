from django.shortcuts import render

from blog_app.models import Category, Post


def home(request):
    posts = Post.objects.all()[:3]
    return render(request, 'home_app/index.html', {'posts': posts})


def sidebar(request):
    categories = Category.objects.all()
    recent_posts = Post.objects.order_by('-created_at')[:3]
    return render(request, 'includes/sidebar.html', {'categories': categories, 'recent_posts': recent_posts})
