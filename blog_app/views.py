# from django.contrib import messages
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.views.generic import ListView, DetailView
# from P_app.models import Post, Like, Comment, Category
#
#
# class Blog(ListView):
#     model = Post
#     template_name = 'blog_app/blog.html'
#     paginate_by = 3
#     context_object_name = 'posts'
#     queryset = Post.objects.order_by('-created_at')
#
#
# class OldestArticle(ListView):
#     model = Post
#     template_name = 'blog_app/blog.html'
#     paginate_by = 3
#     context_object_name = 'posts'
#     queryset = Post.objects.order_by('created_at')
#
#
# class MostVisitedArticle(ListView):
#     model = Post
#     queryset = Post.objects.order_by('-view')
#     template_name = 'blog_app/blog.html'
#     paginate_by = 3
#     context_object_name = 'posts'
#
#
# class LeastVisitedArticle(ListView):
#     model = Post
#     queryset = Post.objects.order_by('view')
#     template_name = 'blog_app/blog.html'
#     paginate_by = 3
#     context_object_name = 'posts'
#
#
# class ArticleDetail(DetailView):
#     model = Post
#     context_object_name = 'post'
#     template_name = 'blog_app/post_details.html'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.view += 1
#         self.object.save()
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         likes_count = Like.objects.filter(post=post).count()
#         context['likes_count'] = likes_count
#         return context
#
#
# def search(request):
#     query = request.GET.get('q')
#     if query == '' or query == None:
#         messages.error(request, 'مقدار سرج نمیتواند خالی باشد')
#         return redirect('blog')
#     posts = Post.objects.filter(title__icontains=query)
#     return render(request, 'blog_app/blog.html', {'posts': posts})
#
#
# def like(request):
#     if request.method == 'POST':
#         post_id = request.POST.get('post')
#         post = Post.objects.get(id=post_id)
#         Like.objects.create(post=post, user=request.user)
#         likes_count = Like.objects.filter(post=post).count()
#         return JsonResponse({'count': likes_count})
#
#
# def remove_like(request):
#     if request.method == 'POST':
#         post_id = request.POST.get('post')
#         post = Post.objects.get(id=post_id)
#         like = Like.objects.filter(post=post, user=request.user).all()
#         like.delete()
#         likes_count = Like.objects.filter(post=post).count()
#         return JsonResponse({'count': likes_count})
#
#
# def comment(request):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         post_slug = request.POST.get('post_slug')
#         post = Post.objects.get(slug=post_slug)
#         user = request.user
#         Comment.objects.create(post=post, user=user, message=message)
#         return redirect('post_detail', slug=post_slug)
#     else:
#         return redirect('home')
#
#
# def reply_comment(request):
#     if request.method == 'POST':
#         comment_id = request.POST.get('comment_id')
#         comment = Comment.objects.get(id=comment_id)
#         user = request.user
#         post_slug = request.POST.get('post_slug')
#         post = Post.objects.get(slug=post_slug)
#         message = request.POST.get('message')
#         Comment.objects.create(user=user, post=post, message=message, reply=comment)
#         return redirect('post_detail', slug=post_slug)
#     else:
#         return redirect('home')
#
#
# def remove_comment(request):
#     if request.method == 'POST':
#         comment_id = request.POST.get('comment_id')
#         reply = Comment.objects.get(id=comment_id)
#         post_slug = request.POST.get('post_slug')
#         reply.delete()
#         return redirect('post_detail', slug=post_slug)
#     else:
#         return redirect('home')
#
#
# def category_detail(request, pk):
#     category = Category.objects.get(id=pk)
#     posts = category.post_set.all()
#     return render(request, 'blog_app/blog.html', {'posts': posts})
