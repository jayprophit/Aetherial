# API Reference Documentation

## Introduction

This document provides a comprehensive reference for the Unified Platform API. The API allows developers to interact with all aspects of the platform programmatically, including social networking, e-commerce, e-learning, job marketplace, and AI features.

## Authentication

### Authentication Methods

The API supports the following authentication methods:

1. **JWT Authentication** - For most API endpoints
2. **API Key Authentication** - For service-to-service communication
3. **OAuth 2.0** - For third-party integrations

### Obtaining Authentication Tokens

#### JWT Authentication

```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 86400
}
```

#### API Key Authentication

API keys can be generated in the developer dashboard:

1. Navigate to Settings > Developer > API Keys
2. Click "Generate New API Key"
3. Set permissions and expiration
4. Store the API key securely

#### Using Authentication

For JWT authentication, include the token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

For API key authentication, include the key in the X-API-Key header:

```
X-API-Key: your-api-key
```

## API Endpoints

### User Management

#### Register User

```
POST /api/auth/register
```

Request body:
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "securepassword",
  "dateOfBirth": "1990-01-01"
}
```

Response:
```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Get Current User

```
GET /api/auth/me
```

Response:
```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "user@example.com",
  "profilePicture": "https://example.com/profile.jpg",
  "dateOfBirth": "1990-01-01",
  "createdAt": "2023-01-01T00:00:00Z",
  "ageVerified": true,
  "kycVerified": false
}
```

#### Update User Profile

```
PUT /api/users/profile
```

Request body:
```json
{
  "name": "John Smith",
  "bio": "Software developer and educator",
  "profilePicture": "data:image/jpeg;base64,..."
}
```

Response:
```json
{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Smith",
  "bio": "Software developer and educator",
  "profilePicture": "https://example.com/profile-updated.jpg",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

### Social Networking

#### Get Posts

```
GET /api/social/posts
```

Query parameters:
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Items per page (default: 20)
- `userId` (optional): Filter by user ID
- `groupId` (optional): Filter by group ID

Response:
```json
{
  "posts": [
    {
      "postId": "123e4567-e89b-12d3-a456-426614174000",
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "userName": "John Doe",
      "userProfilePicture": "https://example.com/profile.jpg",
      "content": "This is a post content",
      "media": [
        {
          "type": "image",
          "url": "https://example.com/image.jpg"
        }
      ],
      "likes": 10,
      "comments": 5,
      "createdAt": "2023-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### Create Post

```
POST /api/social/posts
```

Request body:
```json
{
  "content": "This is a new post",
  "media": [
    {
      "type": "image",
      "data": "data:image/jpeg;base64,..."
    }
  ],
  "visibility": "public"
}
```

Response:
```json
{
  "postId": "123e4567-e89b-12d3-a456-426614174000",
  "content": "This is a new post",
  "media": [
    {
      "type": "image",
      "url": "https://example.com/image.jpg"
    }
  ],
  "visibility": "public",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

### E-commerce

#### Get Products

```
GET /api/ecommerce/products
```

Query parameters:
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Items per page (default: 20)
- `category` (optional): Filter by category
- `search` (optional): Search term
- `minPrice` (optional): Minimum price
- `maxPrice` (optional): Maximum price

Response:
```json
{
  "products": [
    {
      "productId": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Product Name",
      "description": "Product description",
      "price": 99.99,
      "currency": "USD",
      "images": [
        "https://example.com/product1.jpg",
        "https://example.com/product2.jpg"
      ],
      "category": "Electronics",
      "seller": {
        "userId": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Seller Name",
        "rating": 4.5
      },
      "rating": 4.2,
      "reviewCount": 15,
      "inStock": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### Get Product Details

```
GET /api/ecommerce/products/{productId}
```

Response:
```json
{
  "productId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Product Name",
  "description": "Detailed product description",
  "price": 99.99,
  "currency": "USD",
  "images": [
    "https://example.com/product1.jpg",
    "https://example.com/product2.jpg"
  ],
  "category": "Electronics",
  "subcategory": "Smartphones",
  "seller": {
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Seller Name",
    "rating": 4.5,
    "productsCount": 20
  },
  "specifications": {
    "brand": "Brand Name",
    "model": "Model Number",
    "dimensions": "150x70x8mm",
    "weight": "180g"
  },
  "rating": 4.2,
  "reviewCount": 15,
  "reviews": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "userName": "Reviewer Name",
      "rating": 5,
      "comment": "Great product!",
      "createdAt": "2023-01-01T00:00:00Z"
    }
  ],
  "inStock": true,
  "quantity": 10,
  "shippingOptions": [
    {
      "method": "Standard",
      "price": 5.99,
      "estimatedDelivery": "3-5 business days"
    },
    {
      "method": "Express",
      "price": 15.99,
      "estimatedDelivery": "1-2 business days"
    }
  ],
  "relatedProducts": [
    {
      "productId": "223e4567-e89b-12d3-a456-426614174000",
      "name": "Related Product",
      "price": 89.99,
      "image": "https://example.com/related.jpg"
    }
  ],
  "relatedCourses": [
    {
      "courseId": "323e4567-e89b-12d3-a456-426614174000",
      "title": "How to Use This Product",
      "price": 29.99,
      "image": "https://example.com/course.jpg"
    }
  ]
}
```

### E-learning

#### Get Courses

```
GET /api/elearning/courses
```

Query parameters:
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Items per page (default: 20)
- `category` (optional): Filter by category
- `search` (optional): Search term
- `minPrice` (optional): Minimum price
- `maxPrice` (optional): Maximum price
- `difficulty` (optional): Filter by difficulty level

Response:
```json
{
  "courses": [
    {
      "courseId": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Course Title",
      "description": "Course description",
      "price": 49.99,
      "currency": "USD",
      "thumbnail": "https://example.com/course.jpg",
      "category": "Programming",
      "difficulty": "Intermediate",
      "instructor": {
        "userId": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Instructor Name",
        "rating": 4.8
      },
      "rating": 4.5,
      "reviewCount": 120,
      "studentsCount": 1500,
      "duration": "10 hours"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### Job Marketplace

#### Get Job Listings

```
GET /api/jobs/listings
```

Query parameters:
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Items per page (default: 20)
- `category` (optional): Filter by category
- `search` (optional): Search term
- `location` (optional): Filter by location
- `remote` (optional): Filter remote jobs (true/false)
- `minSalary` (optional): Minimum salary
- `maxSalary` (optional): Maximum salary

Response:
```json
{
  "jobs": [
    {
      "jobId": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Software Developer",
      "company": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Company Name",
        "logo": "https://example.com/logo.jpg"
      },
      "location": "New York, NY",
      "remote": true,
      "type": "Full-time",
      "category": "Software Development",
      "salary": {
        "min": 80000,
        "max": 120000,
        "currency": "USD",
        "period": "year"
      },
      "description": "Short job description",
      "requirements": ["JavaScript", "React", "Node.js"],
      "postedAt": "2023-01-01T00:00:00Z",
      "applicantsCount": 25
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### AI Services

#### Chat with AI Assistant

```
POST /api/ai/chat
```

Request body:
```json
{
  "message": "How do I create an online course?",
  "context": {
    "previousMessages": [
      {
        "role": "user",
        "content": "I want to sell my knowledge online"
      },
      {
        "role": "assistant",
        "content": "You could create an online course on our platform."
      }
    ]
  }
}
```

Response:
```json
{
  "response": "To create an online course, follow these steps:\n\n1. Go to the Learning section\n2. Click on 'Create Course'\n3. Fill in the course details\n4. Upload your content\n5. Set pricing\n6. Publish your course\n\nWould you like more detailed instructions for any of these steps?",
  "suggestions": [
    "How do I price my course?",
    "What content formats are supported?",
    "How do I promote my course?"
  ]
}
```

#### Generate Content with AI

```
POST /api/ai/generate-content
```

Request body:
```json
{
  "type": "product-description",
  "parameters": {
    "productName": "Wireless Headphones",
    "features": [
      "Bluetooth 5.0",
      "40-hour battery life",
      "Noise cancellation",
      "Water resistant"
    ],
    "targetAudience": "music enthusiasts",
    "tone": "professional"
  }
}
```

Response:
```json
{
  "content": "Introducing our premium Wireless Headphones, designed specifically for discerning music enthusiasts. Featuring advanced Bluetooth 5.0 technology for seamless connectivity and an impressive 40-hour battery life that keeps your music playing through multiple sessions. The sophisticated noise cancellation system creates an immersive listening experience by blocking out unwanted ambient sounds, while the water-resistant design ensures durability in various environments. Elevate your audio experience with these exceptional headphones that combine cutting-edge technology with superior comfort.",
  "alternatives": [
    {
      "tone": "casual",
      "content": "Meet your new favorite Wireless Headphones! Perfect for music lovers, these awesome headphones come packed with Bluetooth 5.0 for easy connection to all your devices. With a massive 40-hour battery life, you can listen all day (and night) without recharging. The cool noise cancellation feature blocks out annoying background noise, and they're water-resistant too, so a little rain won't stop your music. Ready to experience sound like never before?"
    }
  ]
}
```

### Digital Assets

#### Get User Assets

```
GET /api/assets/balance
```

Response:
```json
{
  "points": 1250,
  "stakedPoints": 500,
  "rewards": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Premium Member Badge",
      "description": "Badge for premium members",
      "image": "https://example.com/badge.jpg",
      "acquiredAt": "2023-01-01T00:00:00Z"
    }
  ],
  "lockedAssets": {
    "points": 750,
    "unlockDate": "2028-01-01T00:00:00Z",
    "reason": "Age restriction - will unlock when user turns 18"
  }
}
```

#### Stake Assets

```
POST /api/assets/stake
```

Request body:
```json
{
  "amount": 100,
  "duration": 30
}
```

Response:
```json
{
  "transactionId": "123e4567-e89b-12d3-a456-426614174000",
  "amount": 100,
  "duration": 30,
  "estimatedReward": 5,
  "unlockDate": "2023-02-01T00:00:00Z",
  "currentBalance": {
    "points": 1150,
    "stakedPoints": 600
  }
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- 200 OK: The request was successful
- 201 Created: The resource was successfully created
- 400 Bad Request: The request was invalid
- 401 Unauthorized: Authentication is required
- 403 Forbidden: The client does not have permission
- 404 Not Found: The resource was not found
- 500 Internal Server Error: An error occurred on the server

Error responses include a JSON object with details:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "The request contains invalid parameters",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- Standard users: 100 requests per minute
- Premium users: 500 requests per minute
- Business accounts: 1000 requests per minute

Rate limit information is included in the response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Webhooks

The API supports webhooks for real-time notifications:

1. Register a webhook endpoint in the developer dashboard
2. Select the events you want to subscribe to
3. Receive real-time notifications when these events occur

Example webhook payload:

```json
{
  "event": "order.created",
  "timestamp": "2023-01-01T00:00:00Z",
  "data": {
    "orderId": "123e4567-e89b-12d3-a456-426614174000",
    "customerId": "123e4567-e89b-12d3-a456-426614174000",
    "amount": 99.99,
    "currency": "USD",
    "status": "pending"
  }
}
```

## SDK Support

The API is supported by official SDKs for the following platforms:

- JavaScript/TypeScript
- Python
- Java
- PHP
- Ruby

Example usage with JavaScript SDK:

```javascript
import { UnifiedPlatformClient } from 'unified-platform-sdk';

const client = new UnifiedPlatformClient({
  apiKey: 'your-api-key'
});

// Get products
client.ecommerce.getProducts({
  category: 'Electronics',
  limit: 10
})
  .then(response => {
    console.log(response.products);
  })
  .catch(error => {
    console.error(error);
  });
```

## API Versioning

The API uses versioning to ensure backward compatibility:

- The current version is v1
- The version is specified in the URL: `/api/v1/resource`
- We maintain backward compatibility within a major version
- We announce deprecations at least 6 months in advance

## Support

For API support, contact:
- Email: api-support@unifiedplatform.com
- Developer Forum: https://developers.unifiedplatform.com/forum
- Documentation: https://developers.unifiedplatform.com/docs
