from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from .models import User, AuctionListing, Bids, BidWinner, Comments, Watchlist


def index(request):
    return render(request, "auctions/index.html")

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

@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        prod = AuctionListing()
        prod.title = request.POST.get('title')
        prod.description = request.POST.get('description')
        prod.price = request.POST.get('price')
        prod.category = request.POST.get('category')
        prod.seller = request.user.username
        if request.POST.get('link'):
            prod.link = request.POST.get('link')
        else:
            prod.link = print("No Image")
        prod.save()
        items = AuctionListing.objects.all()
        none = False
        if len(items) == 0:
            none = True
        return render(request, "auctions/active_listing.html", {
            "none": none,
            "items": items        
        })
    else:
        return render(request, "auctions/create_listing.html")

@login_required(login_url='/login')
def active_listing(request):
    items = AuctionListing.objects.all()
    none = False
    if len(items) == 0:
        none = True
    return render(request, "auctions/active_listing.html", {
        "none": none,
        "items": items,
    })

@login_required(login_url='/login')
def view_listing(request, prod_id):
    comments = Comments.objects.filter(item_id=prod_id)
    if request.method == "POST":
        prod = AuctionListing.objects.get(id=prod_id)
        updated = int(request.POST.get('updated'))
        if prod.price >= updated:
            item = AuctionListing.objects.get(id=prod_id)
            return render(request, "auctions/view_listing.html", {
                "item": item,
                "comments": comments,
                "message": "Bid needs to be higher than current bid."
            })
        else:
            prod.price = updated
            prod.save()
            bid_item = Bids.objects.filter(item_id=prod_id)
            if bid_item:
                bid_item.delete()
            items = Bids()
            items.title = prod.title
            items.user = request.user.username
            items.bids = updated
            items.item_id = prod_id
            items.save()
            items = AuctionListing.objects.get(id=prod_id)
            return render(request, "auctions/view_listing.html", {
                "comments": comments,
                "item": item,
                "message": "Bid updated." 
            })
    else:
        item = AuctionListing.objects.get(id=prod_id)
        new = Watchlist.objects.filter(item_id=prod_id, user=request.user.username)
        return render(request, "auctions/view_listing.html", {
            "comments": comments,
            "item": item,
            "new": new 
        })

@login_required(login_url='/login')
def closed_listing(request):
    final_winner = BidWinner.objects.all()
    none = False
    if len(final_winner) == 0:
        none = True
    return render(request, "auctions/closed_listing.html", {
        "none": none,
        "items": final_winner
    })

@login_required(login_url='/login')
def add_comment(request, prod_id):
    items = Comments()
    items.user = request.user.username
    items.comments = request.POST.get("comment")
    items.item_id = prod_id
    items.save()
    print("comments")
    comments = Comments.objects.filter(item_id=prod_id)
    item = AuctionListing.objects.get(id=prod_id)
    updated = Watchlist.objects.filter(item_id=prod_id, user=request.user.username)
    return render(request, "auctions/view_listing.html", { 
        "comments": comments,
        "item": item,
        "updated": updated
    })

@login_required(login_url='/login')
def close_bid(request, prod_id):
    winning_item = BidWinner()
    listobj = AuctionListing.objects.get(id=prod_id)
    bid_item = Bids.objects.get(item_id=prod_id)
    winning_item = Bids.objects.get(item_id=prod_id)
    winning_item.final_seller = request.user.username
    winning_item.final_winner = bid_item.user
    winning_item.item_id = prod_id
    winning_item.final_price = bid_item.bids
    winning_item.title = bid_item.title
    winning_item.save()
    message = "Closed"
    bid_item.delete()
    if Watchlist.objects.filter(item_id=prod_id):
        watch_item = Watchlist.objects.filter(item_id=prod_id)
        watch_item.delete()
    if Comments.objects.filter(item_id=prod_id):
        comment_item = Comments.objects.filter(item_id=prod_id)
        comment_item.delete()
    listobj.delete()
    won = BidWinner.objects.all()
    none = False
    if len(won) == 0:
        none = True
    return render(request, "auctions/closed_listing.html", {
        "message": message ,
        "items": won,
        "none": none
    })

@login_required(login_url='/login')
def add_watchlist(request, prod_id):
    items = Watchlist.objects.filter(item_id=prod_id, user=request.user.username)
    comment = Comments.objects.filter(item_id=prod_id)
    if items:
        items.delete()
        item = AuctionListing.objects.get(id=prod_id)
        updated = Watchlist.objects.filter(item_id=prod_id, user=request.user.username)
        return render(request, "auctions/view_listing.html", {
            "comment": comment,
            "item": item,
            "updated": updated
        })
    else:
        prod = Watchlist()
        prod.item_id = prod_id
        prod.user = request.user.username
        prod.save()
        item = AuctionListing.objects.get(id=prod_id)
        updated = Watchlist.objects.filter(item_id=prod_id, user=request.user.username)
        return render(request, "auctions/view_listing.html", {
            "item": item,
            "updated": updated,
            "comment": comment
        })

@login_required(login_url='/login')
def categories(request):
    return render(request, "auctions/categories.html")

@login_required(login_url='/login')
def category(request, prod_cat):
    item_cat = AuctionListing.objects.filter(category=prod_cat)
    none = False
    if len(item_cat) == 0:
        none = True
    return render(request, "auctions/category.html", {
        "prod_cat": prod_cat,
        "items": item_cat,
        "none": none
    })

@login_required(login_url='/login')
def watch_list(request):
    final_winners = BidWinner.objects.filter(final_winner=request.user.username)
    lst = Watchlist.objects.filter(user=request.user.username)
    present = False
    prod_list = []
    i = 0
    if lst:
        present = True
        for item in lst:
            items = AuctionListing.objects.get(id=item.item_id)
            prod_list.append(items)
            i += 1
    print(prod_list)
    return render(request, "auctions/watch_list.html", {
        "product_list": prod_list,
        "products": final_winners,       
        "present": present
    })
