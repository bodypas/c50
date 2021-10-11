from django.contrib.auth.models import AbstractUser
from django.db import models

from django.forms import ModelForm


class User(AbstractUser):
    pass

CATEGORIES = (
    ('Appliances', ('Appliances')),
    ('Apps & Games', ('Apps & Games')),
    ('Arts, Crafts, & Sewing', ('Arts, Crafts, & Sewing')),
    ('Automotive Parts & Accessories', ('Automotive Parts & Accessories')),
    ('Baby', ('Baby')),
    ('Beauty & Personal Care', ('Beauty & Personal Care')),
    ('Books', ('Books')),
    ('CDs & Vinyl', ('CDs & Vinyl')),
    ('Cell Phones & Accessories', ('Cell Phones & Accessories')),
    ('Clothing, Shoes and Jewelry', ('Clothing, Shoes and Jewelry')),
    ('Collectibles & Fine Art', ('Collectibles & Fine Art')),
    ('Computers', ('Computers')),
    ('Electronics', ('Electronics')),
    ('Garden & Outdoor', ('Garden & Outdoor')),
    ('Grocery & Gourmet Food', ('Grocery & Gourmet Food')),
    ('Handmade', ('Handmade')),
    ('Health, Household & Baby Care', ('Health, Household & Baby Care')),
    ('Home & Kitchen', ('Home & Kitchen')),
    ('Industrial & Scientific', ('Industrial & Scientific')),
    ('Kindle', ('Kindle')),
    ('Luggage & Travel Gear', ('Luggage & Travel Gear')),
    ('Movies & TV', ('Movies & TV')),
    ('Musical Instruments', ('Musical Instruments')),
    ('Office Products', ('Office Products')),
    ('Sports & Outdoors', ('Sports & Outdoors')),
    ('Tools & Home Improvement', ('Tools & Home Improvement')),
    ('Toys & Games', ('Toys & Games')),
    ('Video Games', ('Video Games')),
    ('None', ('None')),
)

class Bid(models.Model):
    price = models.DecimalField(max_digits=19, decimal_places=2)
    bywhom = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_by_whom")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.bywhom} placed a bid in the amount of {self.price}$"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writtenby")
    text = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.user} left a comment with the following text: {self.text}"

# I know, there are some spelling mistakes through all this project, but left them, because didn't want to be confused later. 

class Listning (models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.CharField(choices=CATEGORIES, default=CATEGORIES[28][0], max_length=64)
    image = models.ImageField(null=True, blank=True, default='default.jpeg' )
    bid = models.ManyToManyField(Bid, blank=True, related_name="bid")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    auction_end = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person} added an item {self.title} with the following price of {self.price}$"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listning = models. ForeignKey(Listning, on_delete=models.CASCADE, related_name="listnings") 

    def __str__(self):
        return f"{self.user} added {self.listning} in his Watchlist"