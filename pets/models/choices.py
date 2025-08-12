from django.db.models import TextChoices

class PetSize(TextChoices):
    SMALL = "small", "Small"
    MEDIUM = "medium", "Medium"
    LARGE = "large", "Large"
    XLARGE = "xlarge", "Extra Large"

class PetStatus(TextChoices):
    AVAILABLE = "available", "Available"
    RESERVED = "reserved", "Reserved"
    SOLD = "sold", "Sold"

class PetGender(TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    UNKNOWN = "unknown", "Unknown"
