from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.Blog.as_view(), name='blog'),
    path('search', views.search, name='search'),
    path('comment', views.comment, name='comment'),
    path('comment-reply', views.reply_comment, name='reply_comment'),
    path('remove-comment', views.remove_comment, name='remove_comment'),
    path('category-detail/<int:pk>', views.category_detail, name='category_detail'),
    path('like', views.like, name='like'),
    path('remove-like', views.remove_like, name='remove_like'),
    path('post-detail/<slug:slug>', views.ArticleDetail.as_view(), name='post_detail'),
]
