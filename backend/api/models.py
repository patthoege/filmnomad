from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    imdb_id = models.CharField(max_length=16, primary_key=True)
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=10, default='movie')  # movie or series
    description = models.TextField(blank=True)
    poster = models.URLField(blank=True)
    director = models.CharField(max_length=200, blank=True)
    rating = models.CharField(max_length=20, blank=True)
    runtime = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('name', 'country')

class Location(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='locations')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='locations')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    visit_info = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class TripPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_plans')
    title = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location, through='TripLocation', related_name='trip_plans')
    created_at = models.DateTimeField(auto_now_add=True)

class TripLocation(models.Model):
    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('trip', 'location')
        ordering = ['order']

class SuggestedLocation(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    movie_title = models.CharField(max_length=200)
    location_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, approved, rejected
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_suggestions')
    reviewed_at = models.DateTimeField(null=True, blank=True)

class AccommodationLink(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=50)
    url = models.URLField()
    description = models.TextField(blank=True)

class FlightsSource(models.Model):
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_from')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_to')
    provider = models.CharField(max_length=50)
    url = models.URLField()