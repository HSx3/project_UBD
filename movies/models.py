from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    vote_average = models.FloatField()
    popularity = models.FloatField()
    poster_url = models.TextField(blank=True)
    backdrop_url = models.TextField(blank=True)
    overview = models.TextField()
    release_date = models.DateField()
    vote_count = models.IntegerField()
    runtime = models.IntegerField(blank=True, null=True)
    video = models.CharField(max_length=255, blank=True)
    movie_genre = models.ManyToManyField(Genre, related_name='genre_movie')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movie', blank=True)
    hate_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='hate_movie', blank=True)
    saw_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_saw', blank=True)
    
class Director(models.Model):
    director_movie = models.ManyToManyField(Movie, related_name='movie_director')
    name = models.CharField(max_length=255)
    profile_path = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=255)
    profile_path = models.TextField(blank=True)
    credit_id = models.CharField(max_length=255)
    cast_id = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.CharField(max_length=255)

class Score(models.Model):
    review = models.CharField(max_length=255, blank=True)
    score = models.FloatField()
    spoiler = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)