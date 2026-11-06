from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster_url = models.URLField(blank=True)
    plot = models.TextField()
    release_date = models.DateField()
    genre = models.JSONField(default=list)
    language = models.CharField(max_length=50)
    runtime_minutes = models.PositiveIntegerField()
    director = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    trailer_url = models.URLField(blank=True, max_length=1000)
    def __str__(self):
        return self.title

class CastMember(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="cast")
    actor_name = models.CharField(max_length=100)
    character_name = models.CharField(max_length=100)
    profile_image = models.URLField(blank=True)
    def __str__(self):
        return self.actor_name

class Review(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="reviews")
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="movie_reviews",null=True,blank=True,)
    def __str__(self):
        return f"{self.reviewer_name} - {self.movie.title}"
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="favorites")
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "movie")
    def __str__(self):
        return f"{self.user} - {self.movie.title}"