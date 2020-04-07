from . import forms
from .models import Post
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def all_posts(request):
    allPosts = Post.objects.all()
    # Implementing searchbar.
    query = request.GET.get("q")
    if query:
        allPosts = allPosts.filter(Q(title__icontains=query)|
                                   Q(body__icontains=query)|
                                   Q(author__username__icontains=query)|
                                   Q(author__first_name__icontains=query)|
                                   Q(author__last_name__icontains=query)).distinct() # Removes duplicate items.
    # Implementing Paginator.
    paginator = Paginator(allPosts, 3) # Shows 3 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'articles/allPosts.html', {'allPosts' : allPosts, 'page_obj': page_obj})

def user_posts(request, user_str):
    allPosts = Post.objects.all()
    allPosts = allPosts.filter(Q(author__username__exact=user_str))
    # Implementing searchbar.
    query = request.GET.get("q")
    if query:
        allPosts = allPosts.filter(Q(title__icontains=query)|
                                   Q(body__icontains=query)|
                                   Q(author__username__icontains=query)|
                                   Q(author__first_name__icontains=query)|
                                   Q(author__last_name__icontains=query)).distinct() # Removes duplicate items.
    # Implementing Paginator.
    paginator = Paginator(allPosts, 3) # Shows 3 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'articles/allPosts.html', {'allPosts' : allPosts, 'page_obj': page_obj})

def detailed_post(request, slug):
    post = Post.objects.get(slug = slug)
    return render(request, 'articles/detailedPost.html', {'post':post})

@login_required() # Decorator which ensures these functions are available only to logged in users.
def create_post(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES) # FILES for image files.
        if form.is_valid():
            instance = form.save(commit = False) # Instance of the post.
            instance.author = request.user
            instance.save() # Saving to database.
            messages.success(request, "Successfully created!") # Success message displayed.
            return redirect('articles:all_posts')
    else:
        form = forms.CreatePost()
    return render(request, 'articles/createPost.html', {'form':form})

@login_required()
def edit_post(request, slug):
    post = Post.objects.get(slug = slug)
    if request.user == post.author:
        if request.method == "POST":
            form = forms.CreatePost(request.POST, request.FILES, instance=post)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                messages.success(request, "Edited succesfully!")
                return redirect('articles:detailed_post',slug=instance.slug)
        else:
            form = forms.CreatePost(instance=post) # Thus, as instance is passed, the form comes preloaded with previous data.
        return render(request, 'articles/editPost.html', {'form': form})

@login_required()
def delete_post(request, slug):
    post_to_delete = Post.objects.get(slug = slug)
    if request.user == post_to_delete.author:
        post_to_delete.delete()
        messages.success(request, "Post deleted") # Post deleted successfully.
        return redirect('articles:all_posts')
