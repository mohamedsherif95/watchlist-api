from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class StreamPlatFormn(models.Model):
    name=models.CharField(max_length=100)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=300)

    def __str__(self):
     return self.name


class Watchlist(models.Model):
    stream=models.ForeignKey(StreamPlatFormn,on_delete=models.CASCADE,related_name="watchlist")
    title=models.CharField(max_length=50)
    storyline=models.CharField(max_length=50)
    active=models.BooleanField(default=True)
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    creatred=models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return self.title

class Review(models.Model):
    user_review=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.CharField(max_length=200)
    watchlist=models.ForeignKey(Watchlist,on_delete=models.CASCADE,related_name="review")
    active=models.BooleanField(default=True)

    def __str__(self):
      return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.user_review)
