"""
Basic InfluenceOS Backend Server
Simple working version for local testing
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI(
    title="InfluenceOS API",
    description="AI-Powered LinkedIn Content Generation Platform",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 InfluenceOS Basic Server Starting...")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_mock_content(topic: str) -> Dict[str, Any]:
    """Generate mock content for testing"""
    return {
        "text": f"🚀 Exciting insights about {topic}!\n\nIn today's rapidly evolving business landscape, understanding {topic} has become crucial for professional success. Here are key takeaways that can transform your approach:\n\n✅ Stay informed about industry trends\n✅ Embrace continuous learning\n✅ Build meaningful professional relationships\n✅ Focus on delivering genuine value\n\nThe future belongs to those who adapt and innovate. By staying ahead of the curve with {topic}, we position ourselves for sustained growth and success.\n\nWhat's your experience with {topic}? Share your thoughts in the comments! 👇",
        "hashtags": ["#LinkedIn", "#Professional", "#Growth", "#Innovation", "#Success", "#Business", "#Leadership", "#Networking"],
        "image_url": get_fallback_image(topic),
        "model_used": "mock"
    }

def get_fallback_image(topic: str) -> str:
    """Get fallback professional image"""
    topic_lower = topic.lower()
    
    if any(word in topic_lower for word in ['ai', 'tech', 'digital', 'innovation']):
        return "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop"
    elif any(word in topic_lower for word in ['business', 'strategy', 'growth']):
        return "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop"
    elif any(word in topic_lower for word in ['leadership', 'team', 'management']):
        return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop"
    else:
        return "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InfluenceOS API - Basic Server",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "basic"
    }

@app.post("/api/v1/pipeline/generate")
async def generate_content(request: Request):
    """Generate content using AI pipeline"""
    try:
        data = await request.json()
        topic = data.get("topic", "Professional Development")
        
        print(f"🎯 Generating content for topic: {topic}")
        
        # Generate content
        result = generate_mock_content(topic)
        
        return {
            "success": True,
            "content": result,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Content generation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Content generation failed"
            }
        )

@app.post("/api/v1/generate-image")
async def generate_image_endpoint(request: Request):
    """Generate image for content"""
    try:
        data = await request.json()
        topic = data.get("topic", "Professional")
        content = data.get("content", "")
        
        print(f"🎨 Generating image for topic: {topic}")
        
        image_url = get_fallback_image(topic)
        
        return {
            "success": True,
            "image_url": image_url,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Image generation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Image generation failed"
            }
        )

@app.get("/api/v1/analytics")
async def get_analytics():
    """Get analytics data"""
    return {
        "success": True,
        "analytics": {
            "total_posts": 25,
            "engagement_rate": 4.2,
            "total_likes": 1250,
            "total_comments": 89,
            "total_shares": 34,
            "growth_rate": 15.3,
            "total_metrics": {
                "likes": 1250,
                "comments": 89,
                "shares": 34,
                "views": 5600,
                "reach": 4200
            },
            "average_metrics": {
                "likes": 62.5,
                "comments": 4.5,
                "shares": 1.7,
                "views": 280,
                "reach": 210
            },
            "growth_trends": {
                "engagement_growth": 15.2,
                "follower_growth": 8.7,
                "reach_growth": 12.3
            },
            "insights": [
                "🎉 Excellent engagement rate! Your content resonates well with your audience.",
                "🕐 Best posting times appear to be Tuesday-Thursday, 9-11 AM",
                "📊 Visual content (carousels, images) tends to perform better",
                "💬 Posts with questions generate 40% more comments"
            ]
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/profile/analyze")
async def analyze_profile():
    """Analyze LinkedIn profile"""
    return {
        "success": True,
        "analysis": {
            "profile_score": 85,
            "completeness": 92,
            "engagement_potential": 78,
            "recommendations": [
                "Add more industry-specific keywords to your headline",
                "Increase posting frequency to 3-4 times per week",
                "Engage more actively with comments on your posts",
                "Share more personal professional stories",
                "Use more visual content (images and carousels)"
            ]
        },
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/v1/profile/connect-linkedin")
async def connect_linkedin(request: Request):
    """Connect LinkedIn account"""
    try:
        data = await request.json()
        auth_code = data.get("auth_code")
        
        return {
            "success": True,
            "message": "LinkedIn account connected successfully",
            "profile": {
                "name": "Professional User",
                "headline": "AI Enthusiast | Content Creator",
                "connections": 1250,
                "followers": 890
            },
            "connected_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "LinkedIn connection failed"
            }
        )

@app.get("/api/v1/outreach/campaigns")
async def get_outreach_campaigns():
    """Get outreach campaigns"""
    return {
        "success": True,
        "campaigns": [
            {
                "id": "campaign_1",
                "name": "Industry Leaders Outreach",
                "status": "active",
                "sent": 45,
                "responses": 12,
                "response_rate": 26.7,
                "created_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": "campaign_2", 
                "name": "Networking Campaign",
                "status": "completed",
                "sent": 78,
                "responses": 23,
                "response_rate": 29.5,
                "created_at": "2024-01-10T14:30:00Z"
            }
        ],
        "total_campaigns": 2,
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/v1/posts/create")
async def create_post(request: Request):
    """Create a new post"""
    try:
        data = await request.json()
        
        post_data = {
            "id": f"post_{datetime.now().timestamp()}",
            "content": data.get("content", ""),
            "scheduled_time": data.get("scheduled_time"),
            "status": "draft",
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "post": post_data,
            "message": "Post created successfully"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Post creation failed"
            }
        )

@app.get("/api/v1/posts")
async def get_posts(limit: int = 10, offset: int = 0):
    """Get posts"""
    return {
        "success": True,
        "posts": [
            {
                "id": "post_1",
                "content": "Sample LinkedIn post about AI trends...",
                "status": "published",
                "engagement": {"likes": 45, "comments": 8, "shares": 3},
                "created_at": "2024-01-15T10:00:00Z"
            }
        ],
        "total": 1,
        "limit": limit,
        "offset": offset,
        "generated_at": datetime.now().isoformat()
    }

# ============================================================================
# SERVER INFO
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting InfluenceOS Basic Server...")
    print("📚 Available endpoints:")
    print("   GET  /              - Root endpoint")
    print("   GET  /health        - Health check")
    print("   POST /api/v1/pipeline/generate - Generate content")
    print("   POST /api/v1/generate-image    - Generate image")
    print("   GET  /api/v1/analytics         - Get analytics")
    print("   GET  /api/v1/profile/analyze   - Analyze profile")
    print("   POST /api/v1/profile/connect-linkedin - Connect LinkedIn")
    print("   GET  /api/v1/outreach/campaigns - Get campaigns")
    print("   POST /api/v1/posts/create      - Create post")
    print("   GET  /api/v1/posts             - Get posts")
    print("")
    print("🔗 Server will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("")
    print("To start the server, run:")
    print("uvicorn basic_server:app --host 0.0.0.0 --port 8000 --reload")
