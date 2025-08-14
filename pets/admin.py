from django.contrib import admin
from .models import Pet, PetPhoto, PetVideo, PetParent, Breed


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'size_category', 'created_at']
    list_filter = ['size_category',]
    search_fields = ['name', 'description']
    ordering = ['name']


class PetPhotoInline(admin.TabularInline):
    model = PetPhoto
    extra = 1
    max_num = 5
    fields = ['image', 'order', 'is_main']


class PetVideoInline(admin.TabularInline):
    model = PetVideo
    extra = 1
    max_num = 2
    fields = ['video', 'title']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'gender', 'size', 'age_months', 'price', 'status', 'featured']
    list_filter = ['breed', 'gender', 'size', 'status', 'featured', 'champions_bloodline']
    search_fields = ['name', 'breed__name', 'size', 'color']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'breed', 'description', 'color', 'weight', 'size', 'gender', 'age_months')
        }),
        ('Breeding & Features', {
            'fields': ('champions_bloodline', 'father', 'mother')
        }),
        ('Status & Pricing', {
            'fields': ('price', 'featured', 'status')
        }),
        ('Health & Documentation', {
            'fields': ('rabies_vaccinated', 'rabies_vaccination_date', 'dhpp_vaccinated', 'dhpp_vaccination_date', 
                      'dewormed', 'deworming_date', 'health_certificate', 'kci_registered', 'registration_number',
                      'microchipped', 'microchip_number', 'health_notes')
        }),
        ('Location & Traits', {
            'fields': ('location', 'lifestyle', 'characteristics')
        }),
    )
    
    inlines = [PetPhotoInline, PetVideoInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing pet
            return ['id', 'created_at', 'updated_at']
        return ['id']


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'order', 'is_main', 'created_at']
    list_filter = ['pet', 'is_main']


@admin.register(PetVideo)
class PetVideoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'title', 'created_at']
    list_filter = ['pet']


@admin.register(PetParent)
class PetParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender',  'registration_number']
    list_filter = ['gender', ]
    search_fields = ['name', 'registration_number']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'gender', 'date_of_birth')
        }),
        ('Registration & Pedigree', {
            'fields': ('registration_number',)
        }),
    )
