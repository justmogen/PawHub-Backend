from django.db import models
from core.models import TimeStampedModel
from .choices import PetGender

class PetParent(TimeStampedModel):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=PetGender.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.gender})"
