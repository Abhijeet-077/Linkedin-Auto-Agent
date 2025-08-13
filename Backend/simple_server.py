#!/usr/bin/env python3
"""
Simple LinkedIn AI Agent Backend Server
Minimal working version for testing
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import asyncio
import json
import uuid
from typing import Dict, Any
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.services.model_manager import model_manager
    MODEL_MANAGER_AVAILABLE = True
except ImportError:
    MODEL_MANAGER_AVAILABLE = False
    print("Model manager not available - using mock responses")

# Create FastAPI app
app = FastAPI(title="LinkedIn AI Agent Backend", version="1.0.0")

# Store active streams
active_streams: Dict[str, Dict[str, Any]] = {}

class PipelineRequest(BaseModel):
    topic: str

class PipelineResponse(BaseModel):
    stream_id: str
    message: str

class SchedulePostRequest(BaseModel):
    text: str
    imageUrl: str = None
    hashtags: list = []
    scheduledTime: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "LinkedIn AI Agent Backend is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "linkedin-ai-agent", "version": "1.0.0"}

@app.get("/test-api.html", response_class=HTMLResponse)
async def get_test_page():
    """Serve the test API page"""
    try:
        with open("test-api.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Test API page not found</h1>", status_code=404)

@app.post("/api/v1/pipeline/generate", response_model=PipelineResponse)
async def generate_content(request: PipelineRequest, background_tasks: BackgroundTasks):
    """Start content generation pipeline"""
    # Generate unique stream ID
    stream_id = str(uuid.uuid4())

    # Initialize stream data
    active_streams[stream_id] = {
        "topic": request.topic,
        "status": "starting",
        "events": []
    }

    # Start background generation task
    background_tasks.add_task(generate_content_pipeline, stream_id, request.topic)

    return PipelineResponse(
        stream_id=stream_id,
        message="Content generation started"
    )

@app.get("/api/v1/pipeline/stream/{stream_id}")
async def stream_pipeline_events(stream_id: str):
    """Stream real-time pipeline events"""
    if stream_id not in active_streams:
        return {"error": "Stream not found"}

    async def event_generator():
        """Generate Server-Sent Events"""
        try:
            while stream_id in active_streams:
                stream_data = active_streams[stream_id]

                # Send any new events
                if stream_data.get("events"):
                    for event in stream_data["events"]:
                        yield f"data: {json.dumps(event)}\n\n"

                    # Clear sent events
                    stream_data["events"] = []

                # Check if stream is complete
                if stream_data.get("status") == "complete":
                    # Clean up after a delay
                    asyncio.create_task(cleanup_stream(stream_id, delay=30))
                    break

                await asyncio.sleep(0.5)  # Check for new events every 500ms

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'payload': {'message': 'Stream error'}})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

@app.get("/api/v1/analytics")
async def get_analytics():
    return {
        "success": True,
        "data": {
            "metrics": [
                {"label": "Total Reach", "value": "12.4K", "change": "+8.2%", "icon": "TrendingUp"},
                {"label": "Followers", "value": "3.2K", "change": "+12.5%", "icon": "Users"},
                {"label": "Engagement", "value": "892", "change": "+15.3%", "icon": "MessageSquare"},
                {"label": "Likes", "value": "2.1K", "change": "+6.7%", "icon": "Heart"},
            ],
            "recentPosts": [
                {"id": 1, "title": "AI in Content Creation", "reach": "1.2K", "engagement": "8.5%", "date": "2 days ago"},
                {"id": 2, "title": "Productivity Tips", "reach": "2.1K", "engagement": "12.3%", "date": "5 days ago"},
            ]
        }
    }

@app.get("/api/v1/profile/analyze")
async def analyze_profile():
    return {
        "success": True,
        "data": {
            "score": 72,
            "recommendations": [
                {"icon": "Camera", "title": "Update profile photo", "description": "Use a high-quality headshot", "priority": "high"},
                {"icon": "FileText", "title": "Enhance bio", "description": "Add more keywords and call-to-action", "priority": "medium"},
            ],
            "stats": [
                {"label": "Bio Optimization", "score": 85, "color": "bg-green-500"},
                {"label": "Content Quality", "score": 78, "color": "bg-blue-500"},
            ]
        }
    }

@app.post("/api/v1/schedule")
async def schedule_post(request: SchedulePostRequest):
    """Schedule a post for publication"""
    return {
        "success": True,
        "schedule_id": f"schedule-{uuid.uuid4()}",
        "message": f"Post scheduled for {request.scheduledTime}",
        "content": {
            "text": request.text,
            "image_url": request.imageUrl,
            "hashtags": request.hashtags,
            "scheduled_time": request.scheduledTime
        }
    }

@app.get("/api/v1/outreach/campaigns")
async def get_outreach_campaigns():
    """Get outreach campaigns"""
    return {
        "success": True,
        "campaigns": [
            {
                "id": "campaign-1",
                "name": "Tech Leaders Outreach",
                "status": "active",
                "sent": 45,
                "responses": 12,
                "response_rate": "26.7%",
                "created_at": "2024-01-15"
            },
            {
                "id": "campaign-2",
                "name": "Startup Founders Network",
                "status": "paused",
                "sent": 23,
                "responses": 8,
                "response_rate": "34.8%",
                "created_at": "2024-01-10"
            }
        ]
    }

@app.post("/api/v1/outreach/campaigns")
async def create_outreach_campaign(request: dict):
    """Create new outreach campaign"""
    return {
        "success": True,
        "campaign_id": f"campaign-{uuid.uuid4()}",
        "message": "Campaign created successfully",
        "campaign": {
            "name": request.get("name", "New Campaign"),
            "message": request.get("message", ""),
            "targets": request.get("targets", []),
            "status": "draft",
            "created_at": "2024-01-20"
        }
    }

@app.get("/api/v1/outreach/templates")
async def get_outreach_templates():
    """Get message templates"""
    return {
        "success": True,
        "templates": [
            {
                "id": "template-1",
                "name": "Professional Introduction",
                "content": "Hi {name}, I came across your profile and was impressed by your work in {industry}. I'd love to connect and share insights about {topic}.",
                "category": "networking"
            },
            {
                "id": "template-2",
                "name": "Collaboration Proposal",
                "content": "Hello {name}, I'm reaching out because I believe we could create something amazing together. Your expertise in {field} aligns perfectly with a project I'm working on.",
                "category": "collaboration"
            }
        ]
    }

@app.post("/api/v1/posts/create")
async def create_new_post(request: dict):
    """Create a new post (for analytics page button)"""
    topic = request.get("topic", "Professional insights")

    # Generate content using the same pipeline
    if MODEL_MANAGER_AVAILABLE:
        try:
            content_data = await model_manager.generate_content(topic)
            return {
                "success": True,
                "post": {
                    "id": f"post-{uuid.uuid4()}",
                    "text": content_data.get("text", ""),
                    "hashtags": content_data.get("hashtags", []),
                    "image_url": content_data.get("image_url", "/placeholder.svg"),
                    "created_at": "2024-01-20T10:00:00Z",
                    "status": "draft"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate content: {str(e)}"
            }
    else:
        return {
            "success": True,
            "post": {
                "id": f"post-{uuid.uuid4()}",
                "text": f"Professional insights about {topic} - generated content would appear here.",
                "hashtags": ["#Professional", "#Insights", "#Growth"],
                "image_url": "/placeholder.svg",
                "created_at": "2024-01-20T10:00:00Z",
                "status": "draft"
            }
        }

@app.post("/api/v1/profile/connect-linkedin")
async def connect_linkedin():
    """Connect LinkedIn account (mock implementation)"""
    return {
        "success": True,
        "message": "LinkedIn connection initiated",
        "auth_url": "https://linkedin.com/oauth/authorize?client_id=mock&redirect_uri=callback",
        "status": "pending"
    }

@app.post("/api/v1/profile/create")
async def create_profile(request: dict):
    """Create user profile"""
    return {
        "success": True,
        "profile": {
            "id": f"profile-{uuid.uuid4()}",
            "name": request.get("name", ""),
            "title": request.get("title", ""),
            "company": request.get("company", ""),
            "industry": request.get("industry", ""),
            "bio": request.get("bio", ""),
            "created_at": "2024-01-20T10:00:00Z"
        },
        "message": "Profile created successfully"
    }

@app.post("/api/v1/generate-image")
async def generate_image(request: dict):
    """Generate image for a given topic"""
    topic = request.get("topic", "Professional business")
    content = request.get("content", "")

    if MODEL_MANAGER_AVAILABLE:
        try:
            # Use the model manager's image generation
            image_url = await model_manager._generate_image_with_openrouter(topic, content)
            return {
                "success": True,
                "image_url": image_url,
                "topic": topic
            }
        except Exception as e:
            # Fallback to placeholder
            image_url = await model_manager._generate_placeholder_image(topic)
            return {
                "success": True,
                "image_url": image_url,
                "topic": topic,
                "note": "Using placeholder image due to generation error"
            }
    else:
        # Mock response
        return {
            "success": True,
            "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop&crop=center&auto=format&q=80",
            "topic": topic,
            "note": "Mock image service"
        }

async def generate_content_pipeline(stream_id: str, topic: str):
    """Background task for content generation using AI models"""
    try:
        stream_data = active_streams[stream_id]

        # Initialize model manager if available
        if MODEL_MANAGER_AVAILABLE:
            if not model_manager.loaded:
                await send_event(stream_id, {
                    "type": "status",
                    "payload": {"step": "initialization", "status": "running"}
                })
                await model_manager.load_models()
                await send_event(stream_id, {
                    "type": "status",
                    "payload": {"step": "initialization", "status": "done"}
                })

        # Step 1: Generate content using AI
        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "draft", "status": "running"}
        })

        if MODEL_MANAGER_AVAILABLE:
            try:
                # Use AI model for content generation (local models or OpenRouter)
                content_data = await model_manager.generate_content(topic)
                content_text = content_data.get("text", "")
                hashtags = content_data.get("hashtags", [])
                image_url = content_data.get("image_url", "/placeholder.svg")
                model_used = content_data.get("model_used", "unknown")

                await send_event(stream_id, {
                    "type": "model_info",
                    "payload": {"model": model_used}
                })

            except Exception as e:
                # Fallback to mock if AI generation fails
                await send_event(stream_id, {
                    "type": "warning",
                    "payload": {"message": f"AI generation failed, using fallback: {str(e)}"}
                })

                content_text = f"""🚀 Exciting insights about {topic}!

Here are the key takeaways that every professional should know:

✨ Innovation drives success in today's competitive landscape
📈 Data-driven decisions lead to better outcomes
🤝 Building strong networks accelerates career growth
💡 Continuous learning is essential for staying relevant

What's your experience with {topic}? I'd love to hear your thoughts in the comments!"""
                hashtags = [f"#{topic.replace(' ', '')}", "#Innovation", "#Leadership", "#Growth", "#Success", "#Business", "#AI"]
                image_url = "/placeholder.svg"
        else:
            # Fallback to mock content
            await asyncio.sleep(2)  # Simulate AI processing
            content_text = f"""🚀 Exciting insights about {topic}!

Here are the key takeaways that every professional should know:

✨ Innovation drives success in today's competitive landscape
📈 Data-driven decisions lead to better outcomes
🤝 Building strong networks accelerates career growth
💡 Continuous learning is essential for staying relevant

What's your experience with {topic}? I'd love to hear your thoughts in the comments!"""
            hashtags = [f"#{topic.replace(' ', '')}", "#Innovation", "#Leadership", "#Growth", "#Success", "#Business", "#AI"]
            image_url = "/placeholder.svg"

        await send_event(stream_id, {
            "type": "text",
            "payload": {"text": content_text}
        })

        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "draft", "status": "done"}
        })

        # Step 2: Generate/process image
        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "image", "status": "running"}
        })

        await asyncio.sleep(1.5)  # Simulate image processing

        await send_event(stream_id, {
            "type": "image",
            "payload": {"url": image_url}
        })

        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "image", "status": "done"}
        })

        # Step 3: Optimize hashtags
        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "hashtags", "status": "running"}
        })

        await asyncio.sleep(1)  # Simulate hashtag optimization

        await send_event(stream_id, {
            "type": "hashtags",
            "payload": {"tags": hashtags}
        })

        await send_event(stream_id, {
            "type": "status",
            "payload": {"step": "hashtags", "status": "done"}
        })

        # Complete
        await send_event(stream_id, {"type": "complete"})
        stream_data["status"] = "complete"

    except Exception as e:
        await send_event(stream_id, {
            "type": "error",
            "payload": {"message": str(e)}
        })
        stream_data["status"] = "error"

async def send_event(stream_id: str, event: Dict[str, Any]):
    """Send event to stream"""
    if stream_id in active_streams:
        active_streams[stream_id]["events"].append(event)

async def cleanup_stream(stream_id: str, delay: int = 0):
    """Clean up stream after delay"""
    if delay > 0:
        await asyncio.sleep(delay)

    if stream_id in active_streams:
        del active_streams[stream_id]

if __name__ == "__main__":
    print("🚀 Starting LinkedIn AI Agent Backend...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🧪 Test Interface: http://localhost:8000/test-api.html")
    print("❤️ Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
