
# InfluenceOS API Documentation

This document provides a detailed description of the InfluenceOS API endpoints.

## Base URL

`http://localhost:8000`

## Authentication

Currently, there is no authentication implemented. All endpoints are open. In a production environment, all endpoints would require authentication.

## Endpoints

### User Profile

#### `POST /api/v1/profile/create`

Creates a new user profile.

**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "avatar_url": "http://example.com/avatar.png",
  "linkedin_profile_url": "http://linkedin.com/in/username",
  "bio": "This is a bio.",
  "industry": "Technology",
  "location": "San Francisco, CA"
}
```

**Response:**

```json
{
  "success": true,
  "user": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "user@example.com",
    "username": "username",
    "created_at": "2025-08-14T12:00:00Z"
  }
}
```

#### `GET /api/v1/profile/analyze`

Analyzes the user's profile and provides recommendations.

**Response:**

```json
{
  "success": true,
  "analysis": {
    "profile_score": 75,
    "completeness": 75,
    "engagement_potential": 78,
    "recommendations": [
      "Add your LinkedIn profile URL to make it easy for people to find you."
    ]
  },
  "generated_at": "2025-08-14T12:00:00Z"
}
```

### Content

#### `POST /api/v1/pipeline/generate`

Generates content using the AI pipeline.

**Request Body:**

```json
{
  "topic": "AI in Business",
  "useIntelligentMode": true
}
```

**Response:**

```json
{
  "success": true,
  "content": {
    "text": "...",
    "hashtags": ["#AI", "#Business"],
    "image_url": "...",
    "model_used": "intelligent-mock"
  },
  "generated_at": "2025-08-14T12:00:00Z"
}
```

#### `POST /api/v1/schedule`

Schedules a post.

**Request Body:**

```json
{
  "text": "This is the content of the post.",
  "imageUrl": "http://example.com/image.png",
  "hashtags": ["#example", "#post"],
  "scheduledTime": "2025-08-21T12:00:00Z"
}
```

**Response:**

```json
{
  "success": true,
  "post": {
    "id": "...",
    "user_id": "...",
    "content": "...",
    "scheduled_time": "...",
    "status": "scheduled"
  }
}
```

#### `GET /api/v1/content/calendar`

Retrieves the content calendar for a user.

**Response:**

```json
{
  "success": true,
  "calendar": {
    "scheduled_posts": [
      {
        "id": "...",
        "user_id": "...",
        "content": "...",
        "scheduled_time": "...",
        "status": "scheduled"
      }
    ]
  }
}
```

### Analytics

#### `GET /api/v1/analytics`

Retrieves analytics data for a user.

**Response:**

```json
{
  "success": true,
  "analytics": {
    "total_posts": 10,
    "total_likes": 500,
    "engagement_rate": 4.2,
    "total_comments": 89,
    "total_shares": 34,
    "growth_rate": 15.3
  },
  "generated_at": "2025-08-14T12:00:00Z"
}
```

### Outreach

#### `POST /api/v1/outreach/campaigns`

Creates a new outreach campaign.

**Request Body:**

```json
{
  "name": "My Campaign",
  "description": "This is a test campaign.",
  "target_audience": "Developers",
  "message_template": "Hello, {name}!"
}
```

**Response:**

```json
{
  "success": true,
  "campaign": {
    "id": "...",
    "user_id": "...",
    "name": "My Campaign",
    "status": "draft",
    "created_at": "2025-08-14T12:00:00Z"
  }
}
```

#### `GET /api/v1/outreach/campaigns`

Retrieves outreach campaigns for a user.

**Response:**

```json
{
  "success": true,
  "campaigns": [
    {
      "id": "...",
      "user_id": "...",
      "name": "My Campaign",
      "status": "draft",
      "created_at": "2025-08-14T12:00:00Z"
    }
  ],
  "generated_at": "2025-08-14T12:00:00Z"
}
```
