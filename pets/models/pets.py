from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from .choices import PetSize, PetStatus, PetGender
from .traits import LifestyleChoices, CharacteristicChoices
from django.contrib.postgres.fields import ArrayField
from .pet_parent import PetParent

class Pet(TimeStampedModel):
    # Basic Information
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kgs")
    size = models.CharField(max_length=10, choices=PetSize.choices, default=PetSize.MEDIUM)
    gender = models.CharField(max_length=10, choices=PetGender.choices, default=PetGender.UNKNOWN)
    age_months = models.PositiveIntegerField(null=True, blank=True)
    champions_bloodline = models.BooleanField(default=False)
    
    # Status and Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=PetStatus.choices, default=PetStatus.AVAILABLE)
    
    # Health & Documentation
    # Core Vaccinations
    rabies_vaccinated = models.BooleanField(default=False, help_text="Rabies vaccination (required by law)")
    rabies_vaccination_date = models.DateField(null=True, blank=True)
    dhpp_vaccinated = models.BooleanField(default=False, help_text="DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza)")
    dhpp_vaccination_date = models.DateField(null=True, blank=True)
    
    # Deworming
    dewormed = models.BooleanField(default=False)
    deworming_date = models.DateField(null=True, blank=True, help_text="Last deworming date")
    
    # Documentation
    health_certificate = models.FileField(upload_to="pets/health_docs/", null=True, blank=True, help_text="Vet health certificate")
    kci_registered = models.BooleanField(default=False, help_text="Kenya Canine Institute registered")
    registration_number = models.CharField(max_length=50, blank=True, help_text="KCI registration number")
    microchipped = models.BooleanField(default=False, help_text="Dog is microchipped")
    microchip_number = models.CharField(max_length=50, blank=True, help_text="Microchip number (if applicable)")
    health_notes = models.TextField(blank=True, help_text="Additional health information")
    
    # Breeder & Location
    # breeder = models.ForeignKey('breeder.Breeder', on_delete=models.CASCADE, related_name='pets')
    location = models.CharField(max_length=100, blank=True )
    
    # Lifestyle & Characteristics
    lifestyle = ArrayField(
        models.CharField(max_length=30, choices=LifestyleChoices.choices),
        default=list,
        blank=True,
    )
    characteristics = ArrayField(
        models.CharField(max_length=30, choices=CharacteristicChoices.choices),
        default=list,
        blank=True,
    )
    
    # Parentage
    father = models.ForeignKey('pets.PetParent', null=True, blank=True, on_delete=models.SET_NULL, related_name='father_of')
    mother = models.ForeignKey('pets.PetParent', null=True, blank=True, on_delete=models.SET_NULL, related_name='mother_of')
    
    @property
    def main_photo(self):
        """Get the main photo for this pet."""
        main = self.photos.filter(is_main=True).first()
        return main.image if main else None
    
    @property
    def is_fully_vaccinated(self):
        """Check if pet has both required vaccinations."""
        return self.rabies_vaccinated and self.dhpp_vaccinated
    
    def __str__(self):
        return f"{self.name} - {self.gender} {self.size}"
    
    class Meta:
        ordering = ['-created_at', 'name']
        indexes = [
            # Search & filtering indexes
            models.Index(fields=['status']),  
            models.Index(fields=['gender', 'size']), 
            models.Index(fields=['price']), 
            models.Index(fields=['location']),  
            models.Index(fields=['featured', 'status']), 
            models.Index(fields=['age_months']), 
            
            # Health & breeding indexes
            models.Index(fields=['rabies_vaccinated', 'dhpp_vaccinated']),
            models.Index(fields=['champions_bloodline']),
            
            # Composite indexes for common queries
            models.Index(fields=['status', 'featured', '-created_at']),
            models.Index(fields=['gender', 'status', 'price']),
        ]


class PetPhoto(TimeStampedModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to="pets/gallery/")
    order = models.PositiveSmallIntegerField(default=0)
    is_main = models.BooleanField(default=False, help_text="Set as main photo")
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def clean(self):
        # Limit to 5 photos per pet
        if self.pet_id and self.pet.photos.count() >= 5 and not self.pk:
            raise ValidationError("Maximum 5 photos allowed per pet.")
        # Only one main photo per pet
        if self.is_main and self.pet_id and self.pet.photos.filter(is_main=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one main photo allowed per pet.")


class PetVideo(TimeStampedModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to="pets/videos/")
    title = models.CharField(max_length=100, blank=True)
    
    def clean(self):
        # Limit to 2 videos per pet
        if self.pet_id and self.pet.videos.count() >= 2 and not self.pk:
            raise ValidationError("Maximum 2 videos allowed per pet.")


