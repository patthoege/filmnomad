from rest_framework import serializers
from .models import Movie, City, Location, TripPlan, TripLocation, SuggestedLocation, AccommodationLink, FlightsSource

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Location
        fields = '__all__'

class LocationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TripLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = TripLocation
        fields = ['id', 'trip', 'location', 'order']

class TripPlanSerializer(serializers.ModelSerializer):
    locations = TripLocationSerializer(source='triplocation_set', many=True, read_only=True)

    class Meta:
        model = TripPlan
        fields = ['id', 'title', 'locations', 'created_at']

class TripPlanWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPlan
        fields = ['id', 'title', 'locations']

class SuggestedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedLocation
        read_only_fields = ['status', 'reviewed_by', 'reviewed_at', 'created_at']
        fields = '__all__'

class AccommodationSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = AccommodationLink
        fields = '__all__'

class FlightsSourceSerializer(serializers.ModelSerializer):
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    class Meta:
        model = FlightsSource
        fields = '__all__'