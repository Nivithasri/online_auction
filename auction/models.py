from django.db import models
from django.utils import timezone
from datetime import datetime

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    zipcode = models.CharField(max_length=6)
    user_name = models.CharField(max_length=20)
    streetno = models.IntegerField()
    streetname = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=12)
    name = models.CharField(max_length=30)
    gmail = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

class Categories(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=25)
    cat_desc = models.CharField(max_length=400)

class Product(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    prod_name = models.CharField(max_length=100)
    prod_desc = models.CharField(max_length=400)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2)
    seller_id = models.IntegerField()
    cat_id = models.IntegerField()
    image = models.ImageField(upload_to='images/') 

class AuctionList(models.Model):
    auc_id = models.IntegerField(primary_key=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    winner_id = models.IntegerField()
    auc_payment = models.DecimalField(max_digits=10, decimal_places=0)
    product_id = models.IntegerField()
    

class Bid(models.Model):
    bidding_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=3)
    prod_id = models.IntegerField()