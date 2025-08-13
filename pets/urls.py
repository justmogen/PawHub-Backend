from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pets.views import PetViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
]

# Available endpoints:
# GET    /api/pets/                    - List all pets (with filtering)
# POST   /api/pets/                    - Create a new pet
# GET    /api/pets/{id}/               - Get pet details
# PUT    /api/pets/{id}/               - Update pet (full)
# PATCH  /api/pets/{id}/               - Update pet (partial)
# DELETE /api/pets/{id}/               - Delete pet
#
# Custom actions:
# GET    /api/pets/featured/           - Get featured pets
# GET    /api/pets/available/          - Get available pets
# GET    /api/pets/champions/          - Get champion bloodline pets
# GET    /api/pets/filters_info/       - Get filter options for frontend
# GET    /api/pets/{id}/photos/        - Get pet photos
# GET    /api/pets/{id}/videos/        - Get pet videos
