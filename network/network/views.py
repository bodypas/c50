from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import User, Post, Comment, Like, Follow, Profile
from. forms import PostForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect,  ensure_csrf_cookie
from django.shortcuts import get_object_or_404



def index(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        for post in posts:
            post.user_liked = post.likes.filter(user=request.user).exists()
    else:
        for post in posts:
            post.user_liked = False
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm()
    return render(request, "network/new_post.html", {
        "form": form
    })
    

@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    following = Follow.objects.filter(user=user).count()
    followers = Follow.objects.filter(following=user).count()
    if request.method == "POST":
        if request.POST["button"] == "Follow":
            try:
                Follow.objects.create(user=request.user, following=user)
            
                return HttpResponseRedirect(reverse("profile", args=[username]))
            except IntegrityError:
                return render(request, "network/profile.html", {
                    "user": user,
                    "posts": posts,
                    "following": following,
                    "followers": followers,
                    "message": "You are already following this user."
                })
        elif request.POST["button"] == "Unfollow":
            Follow.objects.filter(user=request.user, following=user).delete()
            return HttpResponseRedirect(reverse("profile", args=[username]))
        
    return render(request, "network/profile.html", {
        "user": user,
        "page_obj": posts,
        "following": following,
        "followers": followers,
    })
    

@login_required
def show_following(request):
    posts = Post.objects.all()
    following = Follow.objects.filter(user=request.user)
    following_list = []
    for follow in following:
        following_list.append(follow.following)
    following_posts = Post.objects.filter(user__in=following_list)
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


def update_post(request, post_id):
    body = json.loads(request.body)
    updated_content = body.get('content')
    post = Post.objects.get(id=post_id)
    post.content = updated_content
    post.save()
    updated_at = post.updated_at.strftime("%b. %d, %Y, %I:%M %p")
    return JsonResponse({ 'status': 'success', 'updated_at': updated_at })


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_liked = post.likes.filter(user=user).exists()
    if is_liked:
        post.likes.filter(user=user).delete()
    else:
        like = Like.objects.create(post=post, user=user)
    return JsonResponse({'status': 'success', 'like_count': post.likes_count()})


def get_like_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_liked = post.likes.filter(user=user).exists()
    return JsonResponse({'status': 'success', 'is_liked': is_liked})