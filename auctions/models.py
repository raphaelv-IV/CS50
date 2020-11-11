from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    seller = models.CharField(max_length=64, null=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64, null=True) 
    category = models.CharField(max_length=64, null=True) 
    description = models.TextField()
    price = models.IntegerField()
    link = models.CharField(max_length=300, blank=True, null=True, default=None)

class Comments(models.Model):
    item_id = models.IntegerField()
    comment = models.CharField(max_length=64)
    date = models.DateTimeField(null=True)
    user = models.CharField(max_length=64)

class Bids(models.Model):
    title = models.CharField(max_length=64)
    bids = models.IntegerField()
    user = models.CharField(max_length=64)
    item_id = models.IntegerField()

class Watchlist(models.Model):
    item_id = models.IntegerField()
    user = models.CharField(max_length=64)
    
class BidWinner(models.Model):
    final_winner = models.CharField(max_length=64)
    final_price = models.IntegerField()
    final_seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64, null=True)
    item_id = models.IntegerField()