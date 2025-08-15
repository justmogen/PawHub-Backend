from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pets.views import PetViewSet, BreedViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'breeds', BreedViewSet, basename='breed')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
]

# Available endpoints:
# Pets:
# GET    /api/pets/                    - List all pets (with filtering)
# POST   /api/pets/                    - Create a new pet
# GET    /api/pets/{id}/               - Get pet details
# PUT    /api/pets/{id}/               - Update pet (full)
# PATCH  /api/pets/{id}/               - Update pet (partial)
# DELETE /api/pets/{id}/               - Delete pet
#
# Breeds:
# GET    /api/breeds/                  - List all breeds
# GET    /api/breeds/{id}/             - Get breed details
#
# Custom actions:
# GET    /api/pets/filters_info/       - Get filter options for frontend
