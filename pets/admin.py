from django.contrib import admin
from .models.pets import Pet, PetPhoto, PetVideo


class PetPhotoInline(admin.TabularInline):
    model = PetPhoto
    extra = 1
    max_num = 5
    fields = ['image', 'order']


class PetVideoInline(admin.TabularInline):
    model = PetVideo
    extra = 1
    max_num = 2
    fields = ['video', 'title']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'size', 'age_months', 'price', 'status', 'featured']
    list_filter = ['gender', 'size', 'status', 'featured', 'champions_bloodline']
    search_fields = ['name', 'size', 'color']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'color', 'weight', 'size', 'gender', 'age_months')
        }),
        ('Breeding & Features', {
            'fields': ('champions_bloodline',)
        }),
        ('Status & Pricing', {
            'fields': ('price', 'featured', 'status')
        }),
        ('Main Photo', {
            'fields': ('main_photo',)
        }),
    )
    
    inlines = [PetPhotoInline, PetVideoInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing pet
            return ['id', 'created_at', 'updated_at']
        return ['id']


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'order', 'created_at']
    list_filter = ['pet']


@admin.register(PetVideo)
class PetVideoAdmin(admin.ModelAdmin):
    list_display = ['pet', 'title', 'created_at']
    list_filter = ['pet']
