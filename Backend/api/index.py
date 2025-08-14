"""
Vercel Serverless Function Entry Point
Lightweight version of InfluenceOS Backend for Vercel deployment
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Try to import optional dependencies
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="InfluenceOS API",
    description="AI-Powered LinkedIn Content Generation Platform",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# ============================================================================
# MODELS AND SCHEMAS
# ============================================================================

class ContentRequest(BaseModel):
    topic: str
    user_profile: Optional[Dict[str, Any]] = None
    content_type: str = "text"
    target_audience: str = "professional"

class ImageRequest(BaseModel):
    topic: str
    content: str = ""
    style: str = "professional"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def generate_content_with_openrouter(topic: str) -> Dict[str, Any]:
    """Generate content using OpenRouter API"""
    try:
        if not OPENROUTER_API_KEY or not HTTPX_AVAILABLE:
            return generate_mock_content(topic)

        prompt = f"""Create a professional LinkedIn post about: {topic}

Requirements:
- Professional tone suitable for LinkedIn
- 150-250 words
- Include key insights and actionable advice
- End with an engaging question
- No hashtags (will be generated separately)

Topic: {topic}"""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.7
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content_text = data["choices"][0]["message"]["content"].strip()

                return {
                    "text": content_text,
                    "hashtags": generate_hashtags_for_topic(topic),
                    "image_url": get_fallback_image(topic),
                    "model_used": "openrouter-mistral"
                }
            else:
                raise Exception(f"OpenRouter API error: {response.status_code}")

    except Exception as e:
        print(f"Content generation error: {e}")
        return generate_mock_content(topic)

def generate_mock_content(topic: str) -> Dict[str, Any]:
    """Generate mock content for testing"""
    return {
        "text": f"🚀 Exciting insights about {topic}!\n\nIn today's rapidly evolving business landscape, understanding {topic} has become crucial for professional success. Here are key takeaways that can transform your approach:\n\n✅ Stay informed about industry trends\n✅ Embrace continuous learning\n✅ Build meaningful professional relationships\n✅ Focus on delivering genuine value\n\nThe future belongs to those who adapt and innovate. By staying ahead of the curve with {topic}, we position ourselves for sustained growth and success.\n\nWhat's your experience with {topic}? Share your thoughts in the comments! 👇",
        "hashtags": generate_hashtags_for_topic(topic),
        "image_url": get_fallback_image(topic),
        "model_used": "mock"
    }

def generate_hashtags_for_topic(topic: str) -> List[str]:
    """Generate relevant hashtags for a topic"""
    try:
        # Industry-specific hashtag pools
        hashtag_map = {
            "ai": ["#AI", "#ArtificialIntelligence", "#MachineLearning", "#Technology", "#Innovation"],
            "business": ["#Business", "#Leadership", "#Strategy", "#Growth", "#Success"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#Branding", "#SocialMedia"],
            "leadership": ["#Leadership", "#Management", "#TeamBuilding", "#ProfessionalDevelopment", "#Success"],
            "technology": ["#Technology", "#Innovation", "#DigitalTransformation", "#TechTrends", "#Future"],
            "startup": ["#Startup", "#Entrepreneurship", "#Innovation", "#Business", "#Growth"]
        }
        
        topic_lower = topic.lower()
        for key, hashtags in hashtag_map.items():
            if key in topic_lower:
                return hashtags[:5] + ["#LinkedIn", "#Professional", "#Networking"]
        
        # Default hashtags
        return ["#LinkedIn", "#Professional", "#Growth", "#Innovation", "#Success", "#Business", "#Leadership", "#Networking"]
        
    except Exception as e:
        print(f"Hashtag generation error: {e}")
        return ["#LinkedIn", "#Professional", "#Growth", "#Innovation"]

async def generate_image_for_topic(topic: str, content: str = "") -> str:
    """Generate image for topic using Hugging Face or fallback"""
    try:
        # Try Hugging Face Inference API if token is available
        if HUGGINGFACE_TOKEN and HTTPX_AVAILABLE:
            image_url = await generate_image_with_huggingface(topic, content)
            if image_url:
                return image_url

        # Fallback to professional stock images
        return get_fallback_image(topic)

    except Exception as e:
        print(f"Image generation error: {e}")
        return get_fallback_image(topic)

async def generate_image_with_huggingface(topic: str, content: str) -> Optional[str]:
    """Generate image using Hugging Face Inference API"""
    try:
        if not HTTPX_AVAILABLE:
            return None

        prompt = f"Professional LinkedIn post image about {topic}, clean modern business aesthetic, corporate colors, high quality, no text overlay"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
                headers={"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"},
                json={"inputs": prompt},
                timeout=30
            )

            if response.status_code == 200:
                # Convert binary image to base64 data URL
                import base64
                image_data = response.content
                base64_image = base64.b64encode(image_data).decode('utf-8')
                return f"data:image/png;base64,{base64_image}"

        return None

    except Exception as e:
        print(f"Hugging Face image generation error: {e}")
        return None

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
        "message": "InfluenceOS API - Vercel Deployment",
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
        "services": {
            "openrouter": bool(OPENROUTER_API_KEY),
            "huggingface": bool(HUGGINGFACE_TOKEN)
        }
    }

from app.services.content_service import schedule_post, get_scheduled_posts, generate_intelligent_post

@app.post("/api/v1/pipeline/generate")
async def generate_content(request: Request):
    """Generate content using AI pipeline"""
    try:
        data = await request.json()
        topic = data.get("topic", "Professional Development")
        use_intelligent_mode = data.get("useIntelligentMode", False)

        if use_intelligent_mode:
            # In a real app, user email would come from auth session
            user_email = "test@example.com"
            user_profile = get_user_profile(user_email)
            if not user_profile:
                raise HTTPException(status_code=404, detail="User not found")
            result = generate_intelligent_post(topic, user_profile)
        else:
            result = await generate_content_with_openrouter(topic)
        
        return {
            "success": True,
            "content": result,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
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
        
        image_url = await generate_image_for_topic(topic, content)
        
        return {
            "success": True,
            "image_url": image_url,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Image generation failed"
            }
        )

from app.services.analytics_service import get_basic_analytics

@app.get("/api/v1/analytics")
async def get_analytics():
    """Get analytics data"""
    try:
        # In a real app, user_id would come from auth session
        user_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479" # A dummy UUID

        analytics_data = get_basic_analytics(user_id)

        return {
            "success": True,
            "analytics": analytics_data,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve analytics"
            }
        )


from app.services.user_service import create_user, get_user_by_email, get_user_profile

@app.get("/api/v1/profile/analyze")
async def analyze_profile():
    """Analyze LinkedIn profile"""
    try:
        # In a real app, user email would come from auth session
        user_email = "test@example.com" 
        profile = get_user_profile(user_email)

        if not profile:
            # Create a dummy user for demonstration if one doesn't exist
            create_user(email=user_email, username="testuser", full_name="Test User", bio="This is a test bio.")
            profile = get_user_profile(user_email)

        if not profile:
            raise HTTPException(status_code=404, detail="User not found")

        # Simple analysis logic
        recommendations = []
        if not profile.get('bio'):
            recommendations.append("Add a bio to your profile to tell people more about yourself.")
        if not profile.get('linkedin_profile_url'):
            recommendations.append("Add your LinkedIn profile URL to make it easy for people to find you.")
        if not profile.get('industry'):
            recommendations.append("Add your industry to help people understand your area of expertise.")

        profile_score = 100 - (len(recommendations) * 25)

        return {
            "success": True,
            "analysis": {
                "profile_score": profile_score,
                "completeness": 100 - (len(recommendations) * 25),
                "engagement_potential": 78, # static for now
                "recommendations": recommendations if recommendations else ["Your profile is looking great!"],
            },
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Profile analysis failed"
            }
        )


from app.services.user_service import create_user, get_user_by_email

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    avatar_url: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    bio: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None

@app.post("/api/v1/profile/create")
async def create_user_profile(user: UserCreate):
    """Create a new user profile."""
    try:
        existing_user = get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = create_user(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            avatar_url=user.avatar_url,
            linkedin_profile_url=user.linkedin_profile_url,
            bio=user.bio,
            industry=user.industry,
            location=user.location
        )

        if new_user:
            return {"success": True, "user": new_user}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "User profile creation failed"
            }
        )

from app.services.content_service import schedule_post, get_scheduled_posts

class ScheduleRequest(BaseModel):
    text: str
    imageUrl: Optional[str] = None
    hashtags: Optional[List[str]] = None
    scheduledTime: datetime

@app.post("/api/v1/schedule")
async def schedule_post_endpoint(request: ScheduleRequest):
    """Schedule a new post."""
    try:
        # In a real app, user_id would come from auth session
        user_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479" # A dummy UUID
        
        new_post = schedule_post(
            user_id=user_id,
            content=request.text,
            scheduled_time=request.scheduledTime,
            hashtags=request.hashtags,
            image_url=request.imageUrl
        )

        if new_post:
            return {"success": True, "post": new_post}
        else:
            raise HTTPException(status_code=500, detail="Failed to schedule post")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Post scheduling failed"
            }
        )

@app.get("/api/v1/content/calendar")
async def get_content_calendar(user_id: str = Query("f47ac10b-58cc-4372-a567-0e02b2c3d479")):
    """Get scheduled posts for a user."""
    try:
        posts = get_scheduled_posts(user_id)
        return {"success": True, "calendar": {"scheduled_posts": posts}}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve content calendar"
            }
        )

from app.services.outreach_service import get_outreach_campaigns, create_outreach_campaign

class OutreachCampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    message_template: Optional[str] = None

@app.post("/api/v1/outreach/campaigns")
async def create_outreach_campaign_endpoint(campaign: OutreachCampaignCreate):
    """Create a new outreach campaign."""
    try:
        # In a real app, user_id would come from auth session
        user_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479" # A dummy UUID

        new_campaign = create_outreach_campaign(
            user_id=user_id,
            name=campaign.name,
            description=campaign.description,
            target_audience=campaign.target_audience,
            message_template=campaign.message_template
        )

        if new_campaign:
            return {"success": True, "campaign": new_campaign}
        else:
            raise HTTPException(status_code=500, detail="Failed to create outreach campaign")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Outreach campaign creation failed"
            }
        )

@app.get("/api/v1/outreach/campaigns")
async def get_outreach_campaigns_endpoint():
    """Get outreach campaigns"""
    try:
        # In a real app, user_id would come from auth session
        user_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479" # A dummy UUID

        campaigns = get_outreach_campaigns(user_id)

        return {
            "success": True,
            "campaigns": campaigns,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve outreach campaigns"
            }
        )


# Export the app for Vercel
handler = app
