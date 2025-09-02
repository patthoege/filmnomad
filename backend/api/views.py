from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Movie, City, Location, TripPlan, SuggestedLocation, AccommodationLink, FlightsSource, TripLocation
from .serializers import (
    MovieSerializer, CitySerializer, LocationSerializer, LocationWriteSerializer,
    TripPlanSerializer, TripPlanWriteSerializer, SuggestedLocationSerializer,
    AccommodationSerializer, FlightsSourceSerializer
)
from .permissions import IsOwnerOrReadOnly
from django.utils import timezone

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q','')
        type_filter = request.query_params.get('type','')
        qs = Movie.objects.all()
        if type_filter:
            qs = qs.filter(type=type_filter)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(year__icontains=q) | Q(description__icontains=q))
        serializer = MovieSerializer(qs[:20], many=True)
        return Response(serializer.data)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q','')
        qs = City.objects.filter(name__icontains=q) if q else City.objects.all()
        return Response(CitySerializer(qs[:20], many=True).data)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related('movie','city')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        return LocationWriteSerializer if self.action in ['create','update','partial_update'] else LocationSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        city = request.query_params.get('city')
        movie = request.query_params.get('movie')
        qs = self.queryset
        if city:
            qs = qs.filter(city__name__icontains=city)
        if movie:
            qs = qs.filter(movie__title__icontains=movie)
        return Response(LocationSerializer(qs[:50], many=True).data)

class TripPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return TripPlan.objects.filter(user=self.request.user)
    def get_serializer_class(self):
        return TripPlanWriteSerializer if self.action in ['create','update'] else TripPlanSerializer

    def perform_create(self, serializer):
        trip = serializer.save(user=self.request.user)
        location_ids = self.request.data.get('locations', [])
        for order, loc_id in enumerate(location_ids):
            TripLocation.objects.create(trip=trip, location_id=loc_id, order=order)

    def perform_update(self, serializer):
        trip = serializer.save()
        TripLocation.objects.filter(trip=trip).delete()
        location_ids = self.request.data.get('locations', [])
        for order, loc_id in enumerate(location_ids):
            TripLocation.objects.create(trip=trip, location_id=loc_id, order=order)

class SuggestedLocationViewSet(viewsets.ModelViewSet):
    queryset = SuggestedLocation.objects.all().order_by('-created_at')
    serializer_class = SuggestedLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def review(self, request, pk=None):
        suggestion = self.get_object()
        decision = request.data.get('decision')
        if decision not in ['approved','rejected']:
            return Response({'error':'decision must be approved or rejected'}, status=400)
        suggestion.status = decision
        suggestion.reviewed_by = request.user
        suggestion.reviewed_at = timezone.now()
        suggestion.save()
        return Response({'status': suggestion.status})

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = AccommodationLink.objects.all()
    serializer_class = AccommodationSerializer

class FlightsSourceViewSet(viewsets.ModelViewSet):
    queryset = FlightsSource.objects.all()
    serializer_class = FlightsSourceSerializer