# Django Blog API

A Django REST Framework-based blog application with user authentication, blog management, and reporting functionality.

## Features

- **User Management**
  - User registration and authentication
  - Token-based authentication
  - Permission-based access control

- **Blog Management**
  - Create, read, update, and delete blog posts
  - Blog ownership verification
  - Blog activation/deactivation system

- **Reporting System**
  - Report inappropriate blog content
  - Automatic blog deactivation upon reports
  - Admin view for managing reports

- **Web Interface**
  - Simple web view to display all blogs
  - Template-based rendering

## API Endpoints

### Authentication

#### Register User
```
POST /api/register/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
**Response:**
```json
{
  "user_id": 1,
  "user_name": "user@example.com",
  "token": "your_auth_token",
  "message": "User created successfully"
}
```

#### Login User
```
POST /api/login/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
**Response:**
```json
{
  "user_id": 1,
  "username": "user@example.com",
  "token": "your_auth_token",
  "message": "Login successful"
}
```

### Blog Management

#### Create Blog
```
POST /api/blogs/create/
```
**Headers:**
```
Authorization: Token your_auth_token
```
**Request Body:**
```json
{
  "title": "Blog Title",
  "description": "Blog description (max 200 chars)",
  "image": "image_file (optional)",
  "video": "video_file (optional)"
}
```

**Note:** Use `multipart/form-data` for file uploads with images/videos.

#### List All Blogs
```
GET /api/blogs/
```
Returns paginated list of all active blogs.

#### Update Blog
```
PUT /api/blogs/{blog_id}/update/
```
**Headers:**
```
Authorization: Token your_auth_token
```
**Note:** Only the blog owner can update their blog.

#### Delete Blog
```
DELETE /api/blogs/{blog_id}/delete/
```
**Headers:**
```
Authorization: Token your_auth_token
```
**Note:** Only the blog owner can delete their blog.

### Reporting System

#### Report Blog
```
POST /api/blogs/report/
```
**Headers:**
```
Authorization: Token your_auth_token
```
**Request Body:**
```json
{
  "blog": blog_id,
  "reason": "spam",
  "description": "Detailed description of the issue"
}
```

**Available Reason Choices:**
- `spam` - Spam content
- `inappropriate` - Inappropriate Content
- `harassment` - Harassment
- `copyright` - Copyright Violation
- `other` - Other reasons
**Response:**
```json
{
  "message": "Report successfully created and blog deactivated",
  "report_details": {
    "report_id": 1,
    "blog_id": 1,
    "blog_title": "Blog Title",
    "reported_to": "owner@example.com",
    "reason": "spam"
  },
  "action_taken": {
    "blog_deactivated": true,
    "blog_is_now_active": false,
    "deactivation_reason": "report received"
  }
}
```

#### Get Reports List
```
GET /api/reports/
```
Returns list of all reports with detailed information.

## Models

### User (Custom User Model)
- `email`: Unique email field (used as username)
- `is_verified`: Boolean for email verification status
- `is_active`: Boolean for account status
- `is_staff`: Boolean for admin access
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp
- **Features:**
  - Custom UserManager for user creation
  - Auto token generation on user creation
  - Email-based authentication instead of username

### Blog
- `title`: Blog title (max 25 characters)
- `description`: Blog description (max 200 characters)
- `image`: Optional image upload
- `video`: Optional video upload
- `owner`: Foreign key to User
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- **Features:**
  - Ordered by creation date (newest first)
  - Media file support for images and videos

### BlogReport
- `blog`: Foreign key to reported blog
- `reported_by`: User who made the report
- `reason`: Predefined choices (spam, inappropriate, harassment, copyright, other)
- `description`: Optional detailed description
- `created_at`: Report timestamp
- `is_reviewed`: Boolean for admin review status
- **Features:**
  - Unique constraint prevents duplicate reports from same user
  - Predefined reason categories for consistent reporting

### BlacklistedUser
- `user`: OneToOne relationship with User
- `blacklisted_by`: Admin who applied the blacklist
- `reason`: Text field explaining blacklist reason
- `blacklisted_at`: Blacklist timestamp
- `is_active`: Boolean for blacklist status
- **Features:**
  - Tracks who applied the blacklist and when
  - Can be activated/deactivated

## Installation

1. **Clone the repository**
```bash
git clone <repository_url>
cd django-blog-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django
pip install djangorestframework
pip install djangorestframework-authtoken
pip install Pillow  # For image handling
```

4. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run the server**
```bash
python manage.py runserver
```

## Project Structure

```
blogapp/
├── models.py          # User, Blog, BlogReport, BlacklistedUser models
├── serializers.py     # DRF serializers
├── views.py          # API views and web views
├── urls.py           # URL routing
├── templates/
│   └── index.html    # Blog listing template
└── static/
    ├── images/       # Uploaded blog images
    └── videos/       # Uploaded blog videos
```

## Key Features Explained

### Authentication System
- Uses Django REST Framework's token authentication
- Tokens are automatically created upon user registration via Django signals
- Custom User model with email-based authentication
- All blog operations require authentication except viewing

### Blog Management
- Users can only modify their own blogs
- Permission checks ensure data security
- Support for image and video uploads
- Character limits for title (25) and description (200)
- Blogs can be deactivated through the reporting system

### Reporting Mechanism
- Users can report inappropriate content with predefined categories
- Reports automatically deactivate the reported blog
- Prevents duplicate reports from the same user (unique constraint)
- Users cannot report their own blogs
- Admin review tracking with `is_reviewed` field

### User Management
- Custom User model extending AbstractBaseUser
- Email verification system ready
- User blacklisting functionality with detailed tracking
- Admin can manage blacklisted users

### Error Handling
- Comprehensive error responses for various scenarios
- Permission denied errors for unauthorized access
- Validation errors for invalid data
- Integrity error handling for duplicate reports

## Security Features

- Token-based authentication
- Permission classes for different endpoints
- Owner verification for blog operations
- Duplicate report prevention
- Self-reporting prevention

## Dependencies

- Django
- Django REST Framework
- Django REST Framework AuthToken
- Pillow (for image processing)

## Additional Configuration

### Media Files Setup
Add to your `settings.py`:
```python
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# In your main urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # your url patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Custom User Model
In your `settings.py`:
```python
AUTH_USER_MODEL = 'blogapp.User'
```

## Usage Notes

- All authenticated endpoints require the `Authorization: Token <token>` header
- Blog IDs are used in URLs for specific blog operations
- The web interface provides a simple view of all blogs
- Reports automatically deactivate blogs for content moderation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]