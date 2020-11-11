from django.contrib import admin
from .models import User, BidWinner, Bids, Comments, AuctionListing, Watchlist
# Register your models here.
admin.site.register(User)
admin.site.register(BidWinner)
admin.site.register(AuctionListing)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)