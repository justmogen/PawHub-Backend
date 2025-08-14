from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Min, Max
from pets.models import Pet, Breed
from pets.serializers import PetListSerializer, PetDetailSerializer, BreedSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Breed model - read-only operations.
    
    Provides:
    - List view of all available breeds
    - Detail view of specific breed
    """
    queryset = Breed.objects.all().order_by('name')
    serializer_class = BreedSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'size_category', 'created_at']
    ordering = ['name']


class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pet model with CRUD operations.
    
    Provides:
    - List view with filtering and search
    - Detail view with complete pet information
    - Create, Update, Delete operations
    - Custom actions for specific queries
    """
    queryset = Pet.objects.all().select_related('breed', 'father', 'mother').prefetch_related('photos', 'videos')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = {
        'breed': ['exact'],
        'status': ['exact'],
        'gender': ['exact'],
        'size': ['exact'], 
        'featured': ['exact'],
        'price': ['gte', 'lte', 'exact'],
        'age_months': ['gte', 'lte', 'exact'],
        'location': ['icontains'],
        'champions_bloodline': ['exact'],
        'rabies_vaccinated': ['exact'],
        'dhpp_vaccinated': ['exact'],
        'kci_registered': ['exact'],
        'microchipped': ['exact']
    }
    
    # Search options
    search_fields = ['name', 'breed__name', 'color', 'location', 'size', 'status', 'description', 'health_notes']
    # Ordering options
    ordering_fields = ['created_at', 'updated_at', 'name', 'price', 'age_months']
    ordering = ['-featured', '-created_at']  # Featured pets first, then newest
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'list':
            return PetListSerializer
        return PetDetailSerializer
    
    def get_queryset(self):
        """
        Optionally filter the queryset based on query parameters.
        """
        queryset = super().get_queryset()
        
        # Filter by lifestyle choices
        lifestyle = self.request.query_params.get('lifestyle', None)
        if lifestyle:
            # Support multiple lifestyle values separated by comma
            lifestyle_values = lifestyle.split(',')
            queryset = queryset.filter(lifestyle__overlap=lifestyle_values)
        
        # Filter by characteristics
        characteristics = self.request.query_params.get('characteristics', None)
        if characteristics:
            # Support multiple characteristic values separated by comma
            char_values = characteristics.split(',')
            queryset = queryset.filter(characteristics__overlap=char_values)
        
        # Filter by vaccination status
        fully_vaccinated = self.request.query_params.get('fully_vaccinated', None)
        if fully_vaccinated is not None:
            if fully_vaccinated.lower() == 'true':
                queryset = queryset.filter(rabies_vaccinated=True, dhpp_vaccinated=True)
            elif fully_vaccinated.lower() == 'false':
                queryset = queryset.filter(Q(rabies_vaccinated=False) | Q(dhpp_vaccinated=False))
        
        return queryset
      
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get only featured pets.
        """
        featured_pets = self.get_queryset().filter(featured=True, status='available')
        serializer = self.get_serializer(featured_pets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get only available pets.
        """
        available_pets = self.get_queryset().filter(status='available')
        serializer = self.get_serializer(available_pets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def champions(self, request):
        """
        Get pets with champion bloodline.
        """
        champion_pets = self.get_queryset().filter(champions_bloodline=True, status='available')
        serializer = self.get_serializer(champion_pets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def photos(self, request, pk=None):
        """
        Get all photos for a specific pet.
        """
        pet = self.get_object()
        photos = pet.photos.all().order_by('order', 'created_at')
        from pets.serializers.pet_serializers import PetPhotoSerializer
        serializer = PetPhotoSerializer(photos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def videos(self, request, pk=None):
        """
        Get all videos for a specific pet.
        """
        pet = self.get_object()
        videos = pet.videos.all().order_by('created_at')
        from pets.serializers.pet_serializers import PetVideoSerializer
        serializer = PetVideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filters_info(self, request):
        """
        Get available filter options for the frontend.
        """
        from pets.models import PetSize, PetStatus, PetGender, LifestyleChoices, CharacteristicChoices
        
        filter_info = {
            'sizes': [{'value': choice[0], 'label': choice[1]} for choice in PetSize.choices],
            'genders': [{'value': choice[0], 'label': choice[1]} for choice in PetGender.choices],
            'statuses': [{'value': choice[0], 'label': choice[1]} for choice in PetStatus.choices],
            'lifestyles': [{'value': choice[0], 'label': choice[1]} for choice in LifestyleChoices.choices],
            'characteristics': [{'value': choice[0], 'label': choice[1]} for choice in CharacteristicChoices.choices],
            'locations': list(Pet.objects.exclude(location='').values_list('location', flat=True).distinct()),
            'price_range': {
                'min': Pet.objects.filter(price__isnull=False).aggregate(min_price=Min('price'))['min_price'] or 0,
                'max': Pet.objects.filter(price__isnull=False).aggregate(max_price=Max('price'))['max_price'] or 0,
            },
            'age_range': {
                'min': Pet.objects.filter(age_months__isnull=False).aggregate(min_age=Min('age_months'))['min_age'] or 0,
                'max': Pet.objects.filter(age_months__isnull=False).aggregate(max_age=Max('age_months'))['max_age'] or 0,
            }
        }
        return Response(filter_info)
    
    def perform_create(self, serializer):
        """
        Custom create logic if needed.
        """
        # Add any custom logic here (e.g., setting the breeder)
        serializer.save()
    
    def perform_update(self, serializer):
        """
        Custom update logic if needed.
        """
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom delete logic - soft delete or hard delete based on requirements.
        """
        instance = self.get_object()
        
        # Option 1: Soft delete (change status instead of actual deletion)
        # instance.status = 'deleted'
        # instance.save()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        
        # Option 2: Hard delete (current implementation)
        return super().destroy(request, *args, **kwargs)
