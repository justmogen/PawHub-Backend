from rest_framework import serializers
from pets.models import Pet, PetPhoto, PetVideo, PetParent, Breed, LifestyleChoices, CharacteristicChoices


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description', 'size_category']


class PetParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetParent
        fields = ['id', 'name', 'gender', 'date_of_birth', 'registration_number']


class PetListSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    main_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'breed', 'gender', 'age_months',
            'main_photo', 'lifestyle', 'characteristics', 'champions_bloodline'
        ]
        read_only_fields = ['id']
    
    def get_main_photo(self, obj):
        """Get the main photo URL for the pet."""
        main_photo = obj.main_photo
        if main_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_photo.url)
            return main_photo.url
        return None


class PetPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetPhoto
        fields = ['id', 'image', 'order', 'is_main']
        read_only_fields = ['id']


class PetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetVideo
        fields = ['id', 'video', 'title']
        read_only_fields = ['id']


class PetDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Pet detail view.
    Includes all fields and related objects for complete pet information.
    """
    # Related objects
    breed = BreedSerializer(read_only=True)
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), 
        source='breed', 
        write_only=True,
        help_text="Select breed from available options"
    )
    father = PetParentSerializer(read_only=True)
    mother = PetParentSerializer(read_only=True)
    
    # Computed fields
    main_photo = serializers.SerializerMethodField()
    photos = PetPhotoSerializer(many=True, read_only=True)
    videos = PetVideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            # Basic Information
            'id', 'name', 'breed', 'breed_id', 'description', 'color', 'weight', 'size',
            'gender', 'age_months', 'champions_bloodline',
            
            # Status and Pricing
            'price', 'featured', 'status',
            
            # Health & Documentation
            'rabies_vaccinated', 'rabies_vaccination_date',
            'dhpp_vaccinated', 'dhpp_vaccination_date',
            'dewormed', 'deworming_date',
            'health_certificate', 'kci_registered', 'registration_number',
            'microchipped', 'microchip_number', 'health_notes',
            
            # Location
            'location',
            
            # Lifestyle & Characteristics
            'lifestyle', 'characteristics',
            
            # Related objects
            'father', 'mother',
            
            # Computed fields
            'main_photo', 'photos', 'videos',
            
            # Timestamps
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_main_photo(self, obj):
        """Get the main photo URL for the pet."""
        main_photo = obj.main_photo
        if main_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_photo.url)
            return main_photo.url
        return None
    
    def validate_lifestyle(self, value):
        """Validate lifestyle choices."""
        valid_choices = [choice[0] for choice in LifestyleChoices.choices]
        for lifestyle in value:
            if lifestyle not in valid_choices:
                raise serializers.ValidationError(f"'{lifestyle}' is not a valid lifestyle choice.")
        return value
    
    def validate_characteristics(self, value):
        """Validate characteristic choices."""
        valid_choices = [choice[0] for choice in CharacteristicChoices.choices]
        for characteristic in value:
            if characteristic not in valid_choices:
                raise serializers.ValidationError(f"'{characteristic}' is not a valid characteristic choice.")
        return value
    
    def validate(self, attrs):
        """Cross-field validation."""
        # Validate vaccination dates
        if attrs.get('rabies_vaccinated') and not attrs.get('rabies_vaccination_date'):
            raise serializers.ValidationError({
                'rabies_vaccination_date': 'Vaccination date is required when pet is marked as vaccinated.'
            })
        
        if attrs.get('dhpp_vaccinated') and not attrs.get('dhpp_vaccination_date'):
            raise serializers.ValidationError({
                'dhpp_vaccination_date': 'Vaccination date is required when pet is marked as vaccinated.'
            })
        
        # Validate microchip
        if attrs.get('microchipped') and not attrs.get('microchip_number'):
            raise serializers.ValidationError({
                'microchip_number': 'Microchip number is required when pet is marked as microchipped.'
            })
        
        # Validate KCI registration
        if attrs.get('kci_registered') and not attrs.get('registration_number'):
            raise serializers.ValidationError({
                'registration_number': 'Registration number is required when pet is KCI registered.'
            })
        
        return attrs
