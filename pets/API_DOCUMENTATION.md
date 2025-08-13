# Pet API Endpoints

## Overview
The Pet ViewSet provides comprehensive CRUD operations and advanced filtering for the Pet model using Django REST Framework.

## Base URL
```
/api/pets/
```

## Authentication
Currently open access. Authentication will be added for create/update/delete operations when user management is implemented.

## Standard Endpoints

### List Pets
**GET** `/api/pets/`

Returns paginated list of pets with filtering, search, and ordering capabilities.

**Query Parameters:**
- `page` - Page number for pagination
- `page_size` - Number of items per page (max 100)
- `search` - Search in name, description, color, location, health_notes
- `ordering` - Order by: created_at, updated_at, name, price, age_months (prefix with `-` for descending)

**Filtering Options:**
- `status` - exact match (available, sold, reserved)
- `gender` - exact match (male, female, unknown)
- `size` - exact match (small, medium, large, extra_large)
- `featured` - boolean (true/false)
- `price` - gte, lte, exact (e.g., `price__gte=10000&price__lte=50000`)
- `age_months` - gte, lte, exact
- `location` - case-insensitive contains
- `champions_bloodline` - boolean
- `rabies_vaccinated` - boolean
- `dhpp_vaccinated` - boolean
- `kci_registered` - boolean
- `microchipped` - boolean
- `lifestyle` - comma-separated values (active, calm, outdoor, indoor, family_friendly)
- `characteristics` - comma-separated values (friendly, intelligent, loyal, protective, playful)
- `fully_vaccinated` - boolean (requires both rabies and dhpp vaccinations)

**Example:**
```
GET /api/pets/?status=available&size=large&price__lte=30000&featured=true&search=golden
```

### Get Pet Detail
**GET** `/api/pets/{id}/`

Returns complete pet information including photos, videos, and parent details.

### Create Pet
**POST** `/api/pets/`

Create a new pet. Requires all the pet data in JSON format.

### Update Pet
**PUT** `/api/pets/{id}/` - Full update
**PATCH** `/api/pets/{id}/` - Partial update

### Delete Pet
**DELETE** `/api/pets/{id}/`

Permanently removes the pet record.

## Custom Actions

### Featured Pets
**GET** `/api/pets/featured/`

Returns only featured pets that are available.

### Available Pets  
**GET** `/api/pets/available/`

Returns only pets with status "available".

### Champion Bloodline Pets
**GET** `/api/pets/champions/`

Returns available pets with champion bloodline.

### Pet Photos
**GET** `/api/pets/{id}/photos/`

Returns all photos for a specific pet, ordered by display order.

### Pet Videos
**GET** `/api/pets/{id}/videos/`

Returns all videos for a specific pet.

### Filter Information
**GET** `/api/pets/filters_info/`

Returns available filter options for frontend dropdowns:
- Available sizes, genders, statuses
- Lifestyle and characteristic choices  
- Unique locations
- Price and age ranges

## Response Format

### List Response
```json
{
  "count": 150,
  "next": "http://domain.com/api/pets/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "Buddy",
      "description": "Friendly golden retriever",
      "color": "Golden",
      "size": "large",
      "gender": "male",
      "price": "25000.00", 
      "location": "Nairobi",
      "main_photo": "http://domain.com/media/pets/gallery/photo.jpg",
      "is_fully_vaccinated": true,
      "featured": true,
      "status": "available"
    }
  ]
}
```

### Detail Response
```json
{
  "id": "uuid",
  "name": "Buddy",
  "description": "Friendly golden retriever",
  "size": "large",
  "gender": "male",
  "price": "25000.00",
  "rabies_vaccinated": true,
  "rabies_vaccination_date": "2024-01-15",
  "photos": [
    {
      "id": "uuid",
      "image": "http://domain.com/media/pets/gallery/photo1.jpg", 
      "order": 0,
      "is_main": true
    }
  ],
  "father": {
    "id": "uuid",
    "name": "Champion Dad",
    "gender": "male"
  },
  "lifestyle": ["active", "outdoor"],
  "characteristics": ["friendly", "intelligent"]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Performance Notes

- List endpoint uses optimized PetListSerializer for fast loading
- Detail endpoint includes all related data with proper prefetching
- Database indexes are optimized for common filter combinations
- Pagination prevents large result sets

## Next Steps

1. Add authentication and permissions
2. Add rate limiting
3. Add API versioning
4. Add more advanced search capabilities
5. Add bulk operations
