from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import User, Listning, Comment, Bid
from django.shortcuts import redirect
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required

# I know, there are some spelling mistakes through all this project, but left them, because didn't want to be confused later.

@login_required
def auction_close(request, listning_id):
    item_detail = Listning.objects.get(id=listning_id)
    user = User.objects.get(username=request.user)
    if user == item_detail.person:
        item_detail.auction_end = True
        item_detail.save()
        return HttpResponseRedirect(reverse('item_detail', args=(item_detail.id,))) 

@login_required
def comments(request, listning_id):
    item_detail = Listning.objects.get(id=listning_id)
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        comments_form = CommentForm(request.POST)
        if comments_form.is_valid():
            comments = comments_form.save(commit=False)
            comments.user = user
            comments.save()
            item_detail.comments.add(comments)
            item_detail.save()
            return HttpResponseRedirect(reverse('item_detail', args=(item_detail.id,)))
        else:
            return render(request, "auctions/comments.html", {
                "comments_form": comments_form,
                "listning_id": item_detail.id,
                "item_detail": item_detail,
                
            })
    else:
        return render(request, "auctions/comments.html", {
                "comments_form": CommentForm(),
                "listning_id": item_detail.id,
                "item_detail": item_detail,
            })




def category_pick(request, category):
    item_detail = Listning.objects.filter(category=category)
    return render(request, 'auctions/category_pick.html', {
        "category": category,
        "item_detail": item_detail,
    })



def item_detail(request, listning_id):
    item_detail = Listning.objects.get(id=listning_id)
    
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        
        if request.POST.get("button") == "Watchlist":
            if not user.watchlist.filter(listning = item_detail):
                watchlist = Watchlist()
                watchlist.user = user
                watchlist.listning =  item_detail
                watchlist.save()
            else:
                user.watchlist.filter(listning=item_detail).delete()
            return HttpResponseRedirect(reverse('item_detail', args=(item_detail.id,)))
       
        price = float(request.POST["price"])
        bids = item_detail.bid.all()
        
        if price <= item_detail.price:
            return render (request, "auctions/item_detail.html", {
                "message":"Invalid Price. Your bid cannot be lower than current price.",
                "item_detail": item_detail,
                "bid_form":AuctionForm()
})                
        bid_form = AuctionForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.bywhom = user
            bid.save()
            item_detail.bid.add(bid)
            item_detail.price = price
            item_detail.save()
        else:
            return render(request, "auction/item_detail.html", {
                "bid_form":bid_form
            })   
    return render(request, "auctions/item_detail.html",{
        "item_detail": item_detail,
        "bid_form": AuctionForm(),
        
    })        
   

        
@login_required
def watchlist(request):
    user = User.objects.get(username=request.user)
    return render (request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })


def categories(request):
    item_detail = Listning.objects.filter
    return render (request, 'auctions/categories.html', {
        "categories": CATEGORIES,
        "item_detail": item_detail,
        
    })


@login_required
def create(request):
    if request.method == "GET":
        new_page= ListningForm()
        return render(request, "auctions/create.html", {
            "new_page":new_page
        })
    else:
        user = User.objects.get(username=request.user)
        new_page = ListningForm(request.POST, request.FILES)
        if new_page.is_valid():
            listning = new_page.save(commit=False)
            listning.person = user
            listning.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
            "new_page":new_page  })
    
    
          
    


def index(request):
     return render(request, "auctions/index.html",{
        "actlist": Listning.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
