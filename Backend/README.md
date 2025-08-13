# LinkedIn AI Agent Backend

## 🚀 Overview

A comprehensive FastAPI backend for AI-powered LinkedIn content generation and management. This backend provides a complete API suite for content creation, analytics, profile optimization, post scheduling, and outreach campaigns.

## ✨ Features

- **🤖 AI Content Generation**: Real-time content creation with Server-Sent Events
- **📊 Analytics Dashboard**: User metrics and performance tracking
- **👤 Profile Optimization**: AI-powered profile analysis and recommendations
- **📅 Post Scheduling**: Advanced scheduling system with timezone support
- **🎯 Outreach Campaigns**: Automated outreach management
- **🔄 Real-time Updates**: WebSocket and SSE support for live updates
- **🗄️ Database Integration**: Supabase for data persistence
- **⚡ Caching**: Redis for high-performance caching
- **🔒 Security**: Rate limiting, CORS, and input validation

## 🏗️ Architecture

```
Backend/
├── app/
│   ├── api/v1/endpoints/     # API route handlers
│   ├── core/                 # Core configuration and utilities
│   ├── db/                   # Database connections (Supabase, Redis)
│   └── services/             # Business logic and AI services
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── test-api.html            # Interactive API testing interface
└── README.md                # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9+
- Redis (optional, for caching)
- Supabase account (optional, for data persistence)

### Environment Variables

Create a `.env` file in the Backend directory:

```env
# Server Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-here

# Database (Optional)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Redis (Optional)
REDIS_URL=redis://localhost:6379

# AI Models (Optional - for production AI features)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Rate Limiting
RATE_LIMIT_DEFAULT=100
RATE_LIMIT_AI=20
```

### Installation

1. **Install Dependencies**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

2. **Run the Server**
   ```bash
   python main.py
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Interactive Test Suite: http://localhost:8000/test-api.html
   - Health Check: http://localhost:8000/health

## 📚 API Documentation

### Core Endpoints

#### Health Check
- `GET /health` - Server health status

#### Content Generation Pipeline
- `POST /api/v1/pipeline/generate` - Start content generation
- `GET /api/v1/pipeline/stream/{stream_id}` - Real-time progress updates

#### Analytics
- `GET /api/v1/analytics` - User analytics data
- `GET /api/v1/analytics/metrics` - Detailed metrics
- `GET /api/v1/analytics/posts` - Recent posts performance

#### Profile Optimization
- `GET /api/v1/profile/analyze` - Profile analysis
- `GET /api/v1/profile/score` - Optimization score
- `GET /api/v1/profile/recommendations` - Improvement suggestions

#### Post Scheduling
- `POST /api/v1/schedule` - Schedule a post
- `GET /api/v1/schedule` - Get scheduled posts
- `PUT /api/v1/schedule/{id}` - Update scheduled post
- `DELETE /api/v1/schedule/{id}` - Cancel scheduled post

#### Outreach Campaigns
- `GET /api/v1/outreach/campaigns` - List campaigns
- `POST /api/v1/outreach/campaigns` - Create campaign
- `GET /api/v1/outreach/templates` - Message templates

## 🧪 Testing

### Interactive Test Suite

Open `http://localhost:8000/test-api.html` in your browser for a comprehensive testing interface.

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Start content generation
curl -X POST http://localhost:8000/api/v1/pipeline/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI in business"}'
```
