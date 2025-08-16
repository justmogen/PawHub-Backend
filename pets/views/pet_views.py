from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max
from django.core.cache import cache
from pets.models import Pet, Breed, PetSize, PetGender, LifestyleChoices, CharacteristicChoices
from pets.serializers import PetListSerializer, PetDetailSerializer, BreedSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all().order_by('name')
    serializer_class = BreedSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'size_category', 'description']
    ordering_fields = ['name', 'size_category', 'created_at']
    ordering = ['name']


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all().select_related('breed', 'father', 'mother')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = {
        'breed': ['exact'],
        'gender': ['exact'],
        'size': ['exact'], 
        'age_months': ['gte', 'lte', 'exact'],
        'location': ['icontains'],
    }
    
    # Search options
    search_fields = ['name', 'breed__name', 'color', 'location', 'size']
    # Ordering options
    ordering_fields = ['created_at', 'updated_at', 'name', 'age_months']
    ordering = ['-created_at']  # Newest first
    
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
        # Start with base queryset
        if self.action == 'list':
            # For list view, use optimized queryset with only needed fields
            queryset = Pet.objects.all().select_related('breed').only(
                'id', 'name', 'age_months', 'gender', 
                'size', 'location', 'characteristics', 
                'lifestyle', 'champions_bloodline',
                'breed__name'
            )
        else:
            # For detail view and other actions, use full queryset
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
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to add caching for filter responses.
        """
        # Create cache key based on query parameters
        cache_key = f"pets_filters_{hash(str(sorted(request.query_params.items())))}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response(cached_result)
            
        # Get the response from parent
        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=1200)
        
        return response

    @action(detail=False, methods=['get'])
    def filters_info(self, request):
        """
        Get available filter options for the frontend.
        Caches the response
        """
        cache_key = "pets_filters_info"
        cached_info = cache.get(cache_key)
        if cached_info:
            return Response(cached_info)
        
        filter_info = {
            'sizes': [{'value': choice[0], 'label': choice[1]} for choice in PetSize.choices],
            'genders': [{'value': choice[0], 'label': choice[1]} for choice in PetGender.choices],
            'lifestyles': [{'value': choice[0], 'label': choice[1]} for choice in LifestyleChoices.choices],
            'characteristics': [{'value': choice[0], 'label': choice[1]} for choice in CharacteristicChoices.choices],
            'age_range': {
                'min': Pet.objects.filter(age_months__isnull=False).aggregate(min_age=Min('age_months'))['min_age'] or 0,
                'max': Pet.objects.filter(age_months__isnull=False).aggregate(max_age=Max('age_months'))['max_age'] or 0,
            }
        }
        cache.set(cache_key, filter_info, timeout=9200)

    def perform_create(self, serializer):
        """
        Custom create logic if needed.
        Invalidate pet list cache on creation.
        """
        serializer.save()
        # Invalidate all pet list caches
        for key in cache.keys('pets_filters_*'):
            cache.delete(key)
    
    def perform_update(self, serializer):
        """
        Custom update logic if needed.
        Invalidate pet list cache on update.
        """
        serializer.save()
        # Invalidate all pet list caches
        for key in cache.keys('pets_filters_*'):
            cache.delete(key)
    
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
