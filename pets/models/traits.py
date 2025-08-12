from django.db import models

class LifestyleChoices(models.TextChoices):
    APARTMENT_FRIENDLY = "apartment_friendly", "Apartment Friendly"
    FAMILY_FRIENDLY = "family_friendly", "Family Friendly"
    GOOD_WITH_KIDS = "good_with_kids", "Good with Kids"
    GOOD_WITH_OTHER_PETS = "good_with_other_pets", "Good with Other Pets"
    NEEDS_YARD = "needs_yard", "Needs Yard"
    GOOD_FOR_ALLERGIES = "good_for_allergies", "Good for Allergies"
    EXPERIENCED_OWNER = "experienced_owner", "Experienced Owner"

class CharacteristicChoices(models.TextChoices):
    FRIENDLY = "friendly", "Friendly"
    ACTIVE = "active", "Active"
    CALM = "calm", "Calm"
    PROTECTIVE = "protective", "Protective"
    INTELLIGENT = "intelligent", "Intelligent"
    EASY_TO_TRAIN = "easy_to_train", "Easy to Train"
    INDEPENDENT = "independent", "Independent"
    VOCAL = "vocal", "Vocal"
    SHY = "shy", "Shy"
