"""
Supabase Database Integration
"""
import asyncio
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class SupabaseClient:
    """Supabase database client"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        
    async def connect(self) -> None:
        """Initialize Supabase connection"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            logger.warning("Supabase credentials not provided, using mock mode")
            return
            
        try:
            self.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            logger.info("✅ Supabase connection established")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Supabase: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close Supabase connection"""
        if self.client:
            # Supabase client doesn't need explicit disconnection
            self.client = None
            logger.info("Supabase connection closed")
    
    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user analytics data"""
        if not self.client:
            return self._mock_analytics()
            
        try:
            response = self.client.table('user_analytics').select('*').eq('user_id', user_id).execute()
            return response.data[0] if response.data else self._mock_analytics()
        except Exception as e:
            logger.error(f"Error fetching analytics: {e}")
            return self._mock_analytics()
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile analysis"""
        if not self.client:
            return self._mock_profile()
            
        try:
            response = self.client.table('user_profiles').select('*').eq('user_id', user_id).execute()
            return response.data[0] if response.data else self._mock_profile()
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return self._mock_profile()
    
    async def save_generated_content(self, user_id: str, content: Dict[str, Any]) -> str:
        """Save generated content"""
        if not self.client:
            return f"mock-content-{asyncio.get_event_loop().time()}"
            
        try:
            response = self.client.table('generated_content').insert({
                'user_id': user_id,
                'content': content,
                'created_at': 'now()'
            }).execute()
            return response.data[0]['id'] if response.data else f"mock-content-{asyncio.get_event_loop().time()}"
        except Exception as e:
            logger.error(f"Error saving content: {e}")
            return f"mock-content-{asyncio.get_event_loop().time()}"
    
    async def schedule_post(self, user_id: str, content: Dict[str, Any], scheduled_time: str) -> str:
        """Schedule a post"""
        if not self.client:
            return f"mock-schedule-{asyncio.get_event_loop().time()}"
            
        try:
            response = self.client.table('scheduled_posts').insert({
                'user_id': user_id,
                'content': content,
                'scheduled_time': scheduled_time,
                'status': 'scheduled',
                'created_at': 'now()'
            }).execute()
            return response.data[0]['id'] if response.data else f"mock-schedule-{asyncio.get_event_loop().time()}"
        except Exception as e:
            logger.error(f"Error scheduling post: {e}")
            return f"mock-schedule-{asyncio.get_event_loop().time()}"
    
    def _mock_analytics(self) -> Dict[str, Any]:
        """Mock analytics data for development"""
        return {
            "metrics": [
                {"label": "Total Reach", "value": "12.4K", "change": "+8.2%", "icon": "TrendingUp"},
                {"label": "Followers", "value": "3.2K", "change": "+12.5%", "icon": "Users"},
                {"label": "Engagement", "value": "892", "change": "+15.3%", "icon": "MessageSquare"},
                {"label": "Likes", "value": "2.1K", "change": "+6.7%", "icon": "Heart"},
            ],
            "recentPosts": [
                {"id": 1, "title": "AI in Content Creation", "reach": "1.2K", "engagement": "8.5%", "date": "2 days ago"},
                {"id": 2, "title": "Productivity Tips", "reach": "2.1K", "engagement": "12.3%", "date": "5 days ago"},
                {"id": 3, "title": "Future of Work", "reach": "956", "engagement": "6.8%", "date": "1 week ago"},
            ]
        }
    
    def _mock_profile(self) -> Dict[str, Any]:
        """Mock profile data for development"""
        return {
            "score": 72,
            "recommendations": [
                {"icon": "Camera", "title": "Update profile photo", "description": "Use a high-quality headshot", "priority": "high"},
                {"icon": "FileText", "title": "Enhance bio", "description": "Add more keywords and call-to-action", "priority": "medium"},
                {"icon": "Target", "title": "Define target audience", "description": "Specify your ideal follower", "priority": "high"},
                {"icon": "Zap", "title": "Post consistently", "description": "Maintain regular posting schedule", "priority": "low"},
            ],
            "stats": [
                {"label": "Bio Optimization", "score": 85, "color": "bg-green-500"},
                {"label": "Content Quality", "score": 78, "color": "bg-blue-500"},
                {"label": "Posting Frequency", "score": 65, "color": "bg-yellow-500"},
                {"label": "Engagement Rate", "score": 82, "color": "bg-purple-500"},
            ]
        }

# Global instance
supabase_client = SupabaseClient()

async def init_supabase() -> None:
    """Initialize Supabase connection"""
    await supabase_client.connect()

async def get_supabase() -> SupabaseClient:
    """Get Supabase client instance"""
    return supabase_client
