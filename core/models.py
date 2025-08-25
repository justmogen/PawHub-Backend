from django.db import models
import uuid


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating 
    'created_at' and 'updated_at' fields with UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
