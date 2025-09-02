"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views as api_views

router = routers.DefaultRouter()
router.register(r'movies', api_views.MovieViewSet, basename='movie')
router.register(r'cities', api_views.CityViewSet, basename='city')
router.register(r'locations', api_views.LocationViewSet, basename='location')
router.register(r'trips', api_views.TripPlanViewSet, basename='trip')
router.register(r'suggestions', api_views.SuggestedLocationViewSet, basename='suggestion')
router.register(r'accommodations', api_views.AccommodationViewSet, basename='accommodation')
router.register(r'flights', api_views.FlightsSourceViewSet, basename='flight')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]