# PawHub Backend Implementation Flow - Simplified Approach

## Project Overview
Building a Django REST API backend for a pet marketplace focusing on core pet management functionality. Starting with pets CRUD operations using Django admin, then building frontend integration, and finally adding breeder authentication later.

## Simplified Implementation Strategy
**Focus**: Pet management first → Frontend integration → Authentication later
**Approach**: Django admin for initial CRUD → API development → Breeder accounts as final phase

## Core Backend Structure (Simplified)

### **Pet Management (Phase 1 - Current Focus)**
- **Pet CRUD operations** - Create, read, update, delete pets via Django admin
- **Pet model fields** - Name, breed, age, gender, price, description, characteristics, lifestyle tags, location, status
- **Image/video uploads** - Multiple images per pet, optional videos
- **Health records** - Simple vaccination status and health info
- **Status tracking** - Available, reserved, sold

### **API Endpoints (Phase 2)**
- **Public APIs** - Pet listings, pet details (no auth required initially)
- **Search & filtering** - By breed, price range, characteristics, location
- **Pagination** - Handle 12 pets per page for frontend

### **Authentication System (Phase 3 - Later)**
- **Breeder registration/login** - Simple JWT-based auth
- **Breeder profiles** - Basic info (name, business, location, phone)
- **No complex user roles** - Just authenticated breeders vs public users

### **Inquiry System (Phase 4 - Later)**
- **Public inquiry form** - Anyone can submit interest in a pet
- **Customer details capture** - Name, email, phone, location, experience level, living space
- **WhatsApp integration** - Auto-format and send inquiries
- **Inquiry management** - Breeders can view inquiries for their pets

## Implementation Phases

### Phase 1: Pet Models & Django Admin (Current)
1. **Django Project Structure**
   ```
   pethub/              # Main project
   ├── settings.py      # Simple single settings file for now
   ├── __init__.py
   ├── urls.py
   ├── wsgi.py
   └── asgi.py
   
   pets/               # Single pets app initially
   ├── models.py       # Pet, Breed models
   ├── admin.py        # Django admin configuration
   ├── views.py        # API views (later)
   ├── serializers.py  # DRF serializers (later)
   └── urls.py         # API URLs (later)
   ```

2. **Initial Configuration**
   - Basic Django setup with PostgreSQL
   - Django admin interface
   - Media files configuration for images
   - Basic DRF setup for future API development

3. **Pet Models (Simplified)**
   - **Pet**: Core model with all necessary fields
   - **Breed**: Simple breed reference (can expand later)
   - Focus on essential fields, add complexity later

### Phase 2: API Development & Frontend Integration
**Order: Pet APIs → Frontend Integration → Testing**

1. **Pet APIs** (Public access initially)
   - `GET /api/pets/` - List pets with filtering & pagination
   - `GET /api/pets/{id}/` - Pet details
   - **Filtering**: breed, price_range, characteristics, location
   - **Pagination**: 12 pets per page

2. **Frontend Integration**
   - Connect Next.js frontend to Django APIs
   - Test pet listings and detail pages
   - Implement search and filtering
   - Handle image serving

### Phase 3: Authentication & Breeder Management (Later)
1. **Simple Authentication**
   - JWT token authentication
   - Basic User model extension
   - Breeder profile management

2. **Breeder Pet Management**
   - `POST /api/pets/` - Create pet
   - `PUT /api/pets/{id}/` - Update pet
   - `DELETE /api/pets/{id}/` - Delete pet
   - `GET /api/my-pets/` - List breeder's pets

### Phase 4: Inquiry System (Final)
1. **Customer Inquiries**
   - Public inquiry submission
   - Breeder inquiry management
   - WhatsApp integration

## Recommended Implementation Order (Simplified)

### Week 1: Pet Models & Admin (Current Focus)
1. Django project setup (single app approach)
2. Pet and Breed models
3. Django admin configuration for CRUD operations
4. Database migrations and basic data entry

### Week 2: API Development
1. DRF setup and configuration
2. Pet serializers and viewsets
3. Public pet listing and detail APIs
4. Basic filtering and pagination

### Week 3: Frontend Integration
1. Connect Next.js to Django APIs
2. Test pet listings and detail pages
3. Implement search and filtering
4. Image serving and handling

### Week 4: Authentication (Later Phase)
1. JWT authentication setup
2. Breeder user model
3. Protected pet management endpoints
4. Breeder-specific pet CRUD

### Week 5: Inquiry System (Final Phase)
1. Inquiry models and APIs
2. WhatsApp integration
3. Breeder inquiry management
4. Final polish and testing

## Pet Model Structure (Simplified)

### Core Pet Fields (Phase 1)
```python
class Pet(models.Model):
    # Basic Info
    name = CharField(max_length=100)
    breed = CharField(max_length=100)  # Simple string initially, FK later
    age_months = IntegerField(null=True, blank=True)
    gender = CharField(choices=[('male', 'Male'), ('female', 'Female')])
    price = DecimalField(max_digits=10, decimal_places=2)
    
    # Description & Details
    description = TextField()
    characteristics = JSONField(default=list)  # ['friendly', 'active']
    lifestyle = JSONField(default=list)        # ['family', 'apartment']
    location = CharField(max_length=200)
    
    # Status & Availability
    status = CharField(choices=[
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    ], default='available')
    
    # Media
    main_photo = ImageField(upload_to='pets/photos/')
    photo_gallery = JSONField(default=list)  # List of image URLs
    
    # Health (Simplified)
    vaccinated = BooleanField(default=False)
    health_notes = TextField(blank=True)
    
    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

## API Response Format (Simplified)

### Pet List Response
```json
{
  "count": 156,
  "next": "http://localhost:8000/api/pets/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Bella",
      "breed": "Golden Retriever",
      "main_photo": "http://localhost:8000/media/pets/photos/bella_main.jpg",
      "age_months": 8,
      "gender": "female",
      "price": "1200.00",
      "characteristics": ["friendly", "active"],
      "lifestyle": ["family", "active"],
      "location": "New York",
      "status": "available",
      "description": "Beautiful golden retriever puppy..."
    }
  ]
}
```

## Current Phase Focus

### Immediate Tasks (This Week)
1. **Create Pet Model** - Simple but complete model in `pets/models.py`
2. **Configure Django Admin** - Rich admin interface for pet management
3. **Add Sample Data** - Create test pets through admin
4. **Test Media Upload** - Ensure image upload works

### Next Phase (Following Week)
1. **Create Pet APIs** - DRF viewsets for pet CRUD
2. **Add Filtering** - Price, breed, location, characteristics
3. **Test with Frontend** - Connect Next.js app
4. **Handle CORS** - Ensure frontend can access APIs

### Success Metrics (Current Phase)
- [ ] Pet model created and migrated
- [ ] Django admin showing pets with images
- [ ] Can create/edit pets through admin
- [ ] Image upload working
- [ ] Basic data structure matches frontend needs

This simplified approach focuses on getting core functionality working quickly, then building authentication and advanced features later.
