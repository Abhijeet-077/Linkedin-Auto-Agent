#!/usr/bin/env python3
"""
Working InfluenceOS Backend Server
Guaranteed to work for local development
"""

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

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("InfluenceOS Working Server Starting...")
print("Server will be available at: http://localhost:8000")
print("API docs will be available at: http://localhost:8000/docs")

# ============================================================================
# CONTENT GENERATION
# ============================================================================

def generate_professional_content(topic: str) -> Dict[str, Any]:
    """Generate professional LinkedIn content"""

    # Enhanced topic-specific content templates
    content_templates = {
        "ai": f"",
        
        "business": f"",
        
        "leadership": f"",
        
        "technology": f""
    }
    
    # Determine content type based on topic
    topic_lower = topic.lower()
    
    if any(word in topic_lower for word in ['ai', 'artificial', 'machine', 'automation']):
        content = content_templates["ai"]
        hashtags = ["#AI", "#ArtificialIntelligence", "#Innovation", "#Technology", "#DigitalTransformation", "#MachineLearning", "#LinkedIn", "#Professional"]
    elif any(word in topic_lower for word in ['business', 'strategy', 'growth', 'market', 'sales']):
        content = content_templates["business"]
        hashtags = ["#Business", "#Strategy", "#Growth", "#Leadership", "#Success", "#Innovation", "#LinkedIn", "#Professional"]
    elif any(word in topic_lower for word in ['leadership', 'management', 'team', 'culture']):
        content = content_templates["leadership"]
        hashtags = ["#Leadership", "#Management", "#TeamBuilding", "#Culture", "#ProfessionalDevelopment", "#Success", "#LinkedIn", "#Professional"]
    elif any(word in topic_lower for word in ['tech', 'digital', 'software', 'data']):
        content = content_templates["technology"]
        hashtags = ["#Technology", "#Innovation", "#DigitalTransformation", "#TechTrends", "#Software", "#Data", "#LinkedIn", "#Professional"]
    else:
        # Default professional content
        content = f""
        hashtags = ["#Professional", "#Growth", "#Success", "#Innovation", "#LinkedIn", "#Networking", "#CareerDevelopment", "#Business"]
    
    # Get appropriate image
    image_url = get_professional_image(topic)
    
    return {
        "text": content,
        "hashtags": hashtags,
        "image_url": image_url,
        "model_used": "professional_template"
    }

def get_professional_image(topic: str) -> str:
    """Get professional image based on topic with enhanced selection"""
    import random

    topic_lower = topic.lower()

    # AI/Technology images - Modern tech and innovation
    if any(word in topic_lower for word in ['ai', 'artificial', 'tech', 'digital', 'innovation', 'software', 'data', 'automation']):
        images = [
            "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop&auto=format",  # Tech background
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=600&fit=crop&auto=format",  # Digital network
            "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=600&fit=crop&auto=format",  # Modern workspace
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=600&fit=crop&auto=format",  # Code and tech
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=600&fit=crop&auto=format"   # AI visualization
        ]
    # Business/Strategy images - Professional business environments
    elif any(word in topic_lower for word in ['business', 'strategy', 'growth', 'market', 'finance', 'sales', 'revenue']):
        images = [
            "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop&auto=format",  # Business meeting
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop&auto=format",  # Office workspace
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&h=600&fit=crop&auto=format",  # Business discussion
            "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800&h=600&fit=crop&auto=format",  # Team collaboration
            "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=600&fit=crop&auto=format"   # Business growth
        ]
    # Leadership/Team images - Leadership and collaboration
    elif any(word in topic_lower for word in ['leadership', 'team', 'management', 'culture', 'collaboration', 'communication']):
        images = [
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop&auto=format",  # Team meeting
            "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=800&h=600&fit=crop&auto=format",  # Business team
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=600&fit=crop&auto=format",  # Collaboration
            "https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800&h=600&fit=crop&auto=format",  # Leadership
            "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800&h=600&fit=crop&auto=format"   # Team success
        ]
    # Marketing/Social Media images
    elif any(word in topic_lower for word in ['marketing', 'social', 'content', 'brand', 'audience', 'engagement']):
        images = [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&auto=format",  # Marketing analytics
            "https://images.unsplash.com/photo-1533750516457-a7f992034fec?w=800&h=600&fit=crop&auto=format",  # Content creation
            "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=800&h=600&fit=crop&auto=format",  # Social media
            "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=600&fit=crop&auto=format",  # Digital marketing
            "https://images.unsplash.com/photo-1553028826-f4804a6dba3b?w=800&h=600&fit=crop&auto=format"   # Brand strategy
        ]
    # Professional/General images - Clean professional aesthetics
    else:
        images = [
            "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop&auto=format",  # Professional workspace
            "https://images.unsplash.com/photo-1486312338219-ce68e2c6b696?w=800&h=600&fit=crop&auto=format",  # Modern office
            "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=800&h=600&fit=crop&auto=format",  # Business professional
            "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=600&fit=crop&auto=format",  # Professional meeting
            "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800&h=600&fit=crop&auto=format"   # Professional success
        ]

    # Return random image from appropriate category
    return random.choice(images)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InfluenceOS API - Working Server",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "GET /health",
            "POST /api/v1/pipeline/generate",
            "POST /api/v1/generate-image",
            "GET /api/v1/analytics",
            "GET /api/v1/profile/analyze",
            "GET /api/v1/outreach/campaigns"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "working",
        "version": "2.0.0"
    }

@app.post("/api/v1/pipeline/generate")
async def generate_content(request: Request):
    """Generate content using AI pipeline"""
    try:
        data = await request.json()
        topic = data.get("topic", "Professional Development")
        
        print(f"")
        
        # Generate professional content
        result = generate_professional_content(topic)
        
        print(f"")
        
        return {
            "success": True,
            "content": result,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"")
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
        
        print(f"")
        
        image_url = get_professional_image(topic)
        
        return {
            "success": True,
            "image_url": image_url,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"")
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
            "insights": [
                "",
                "",
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

@app.get("/api/v1/analytics/engagement")
async def get_engagement_analytics():
    """Get engagement analytics for Dashboard"""
    return {
        "success": True,
        "analytics": {
            "total_posts": 25,
            "total_likes": 1250,
            "total_comments": 89,
            "total_shares": 34,
            "total_views": 5600,
            "engagement_rate": 4.2,
            "growth_rate": 15.3,
            "insights": [
                "",
                "",
                "📊 Visual content (carousels, images) tends to perform better"
            ]
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/engagement/analytics")
async def get_engagement_analytics_alt():
    """Alternative endpoint for engagement analytics"""
    return {
        "success": True,
        "analytics": {
            "total_posts": 25,
            "total_likes": 1250,
            "total_comments": 89,
            "total_shares": 34,
            "total_views": 5600,
            "engagement_rate": 4.2,
            "growth_rate": 15.3,
            "reach": 4200,
            "impressions": 8500,
            "click_through_rate": 2.8,
            "insights": [
                "",
                "",
                "📊 Visual content (carousels, images) tends to perform better",
                "💬 Posts with questions generate 40% more comments"
            ]
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/calendar/content")
async def get_content_calendar():
    """Get content calendar data"""
    return {
        "success": True,
        "calendar": {
            "scheduled_posts": [
                {
                    "id": "post_1",
                    "title": "AI Trends in Business",
                    "scheduled_time": "2024-01-16T09:00:00Z",
                    "status": "scheduled",
                    "content_type": "text"
                },
                {
                    "id": "post_2",
                    "title": "Leadership Insights",
                    "scheduled_time": "2024-01-17T14:00:00Z",
                    "status": "draft",
                    "content_type": "carousel"
                }
            ],
            "total_scheduled": 2
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/analytics/optimal-times")
async def get_optimal_posting_times():
    """Get optimal posting times"""
    return {
        "success": True,
        "optimal_times": [
            {"day": "Monday", "time": "09:00", "engagement_score": 85},
            {"day": "Tuesday", "time": "10:00", "engagement_score": 92},
            {"day": "Wednesday", "time": "09:30", "engagement_score": 88},
            {"day": "Thursday", "time": "11:00", "engagement_score": 90},
            {"day": "Friday", "time": "08:30", "engagement_score": 78}
        ],
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

@app.get("/api/v1/engagement/analytics")
async def get_engagement_analytics_dashboard(user_id: str = "default", time_period: str = "30d"):
    """Get engagement analytics for Dashboard"""
    return {
        "success": True,
        "analytics": {
            "total_metrics": {
                "likes": 1250,
                "comments": 89,
                "shares": 34,
                "views": 5600,
                "reach": 4200
            },
            "average_metrics": {
                "likes": 50.0,
                "comments": 3.6,
                "shares": 1.4,
                "views": 224.0,
                "reach": 168.0
            },
            "engagement_rate": 4.2,
            "total_posts": 25,
            "growth_trends": {
                "engagement_growth": 15.3,
                "follower_growth": 8.7,
                "reach_growth": 12.1
            },
            "insights": [
                "",
                "",
                "📊 Visual content (carousels, images) tends to perform better",
                "💬 Posts with questions generate 40% more comments"
            ]
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/content/calendar")
async def get_content_calendar_dashboard(start_date: str = None, end_date: str = None, user_id: str = "default"):
    """Get content calendar data for Dashboard"""
    return {
        "success": True,
        "calendar": {
            "scheduled_posts": [
                {
                    "id": "post_1",
                    "content": {
                        "text": "AI Trends in Business: How artificial intelligence is transforming modern enterprises..."
                    },
                    "scheduled_time": "2024-01-16T09:00:00Z",
                    "post_type": "text",
                    "status": "scheduled"
                },
                {
                    "id": "post_2",
                    "content": {
                        "text": "Leadership Insights: Building effective teams in the digital age requires..."
                    },
                    "scheduled_time": "2024-01-17T14:00:00Z",
                    "post_type": "carousel",
                    "status": "draft"
                }
            ],
            "total_scheduled": 2
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/content/optimal-times")
async def get_optimal_times_dashboard(industry: str = "Technology", role: str = "Professional", target_audience: str = "professional"):
    """Get optimal posting times for Dashboard"""
    return {
        "success": True,
        "optimal_times": [
            {"day": "Monday", "time": "09:00", "engagement_score": 85},
            {"day": "Tuesday", "time": "10:00", "engagement_score": 92},
            {"day": "Wednesday", "time": "09:30", "engagement_score": 88},
            {"day": "Thursday", "time": "11:00", "engagement_score": 90},
            {"day": "Friday", "time": "08:30", "engagement_score": 78}
        ],
        "generated_at": datetime.now().isoformat()
    }

# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n🎯 Starting InfluenceOS Working Server...")
    print("📋 Available endpoints:")
    print("   GET  /              - Root endpoint")
    print("   GET  /health        - Health check")
    print("   POST /api/v1/pipeline/generate - Generate content")
    print("   POST /api/v1/generate-image    - Generate image")
    print("   GET  /api/v1/analytics         - Get analytics")
    print("   GET  /api/v1/profile/analyze   - Analyze profile")
    print("   GET  /api/v1/outreach/campaigns - Get campaigns")
    print("")
    
    uvicorn.run(
        "working_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
