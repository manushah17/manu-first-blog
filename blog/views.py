from django.shortcuts import render
from django.utils import timezone
from .models import Blog
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404


def post_list(request):
    blogs = Blog.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/blog_index.html', {'blogs':blogs})


def post_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/post_detail.html', {'blog': blog})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.published_date = timezone.now()
            blog.save()
            return redirect('post_detail', pk=blog.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.published_date = timezone.now()
            blog.save()
            return redirect('post_detail', pk=blog.pk)
    else:
        form = PostForm(instance=blog)
    return render(request, 'blog/post_edit.html', {'form': form})


