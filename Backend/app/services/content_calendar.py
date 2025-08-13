"""
Content Calendar Service
Visual calendar management for scheduled posts and content planning
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, date
from app.core.logger import get_logger

logger = get_logger(__name__)

class ContentCalendarService:
    """Content calendar management and scheduling service"""
    
    def __init__(self):
        self.scheduled_posts = {}
        self.content_templates = {}
        
    async def get_calendar_view(
        self, 
        start_date: str, 
        end_date: str,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """Get calendar view with scheduled posts"""
        try:
            logger.info(f"📅 Getting calendar view from {start_date} to {end_date}")
            
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
            # Get scheduled posts in date range
            scheduled_posts = await self._get_scheduled_posts(start, end, user_id)
            
            # Generate calendar data
            calendar_data = await self._generate_calendar_data(start, end, scheduled_posts)
            
            # Get content suggestions for empty slots
            suggestions = await self._get_content_suggestions(start, end, user_id)
            
            return {
                "calendar_data": calendar_data,
                "scheduled_posts": scheduled_posts,
                "content_suggestions": suggestions,
                "total_posts": len(scheduled_posts),
                "date_range": {
                    "start": start_date,
                    "end": end_date
                },
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Calendar view generation failed: {e}")
            return await self._get_fallback_calendar()
    
    async def schedule_post(
        self,
        content: Dict[str, Any],
        scheduled_time: str,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """Schedule a post for future publication"""
        try:
            logger.info(f"📝 Scheduling post for {scheduled_time}")
            
            post_id = f"post_{datetime.now().timestamp()}"
            scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
            
            post_data = {
                "id": post_id,
                "content": content,
                "scheduled_time": scheduled_time,
                "status": "scheduled",
                "created_at": datetime.now().isoformat(),
                "user_id": user_id,
                "post_type": content.get("type", "text"),
                "estimated_engagement": await self._estimate_engagement(content, scheduled_dt)
            }
            
            # Store scheduled post
            if user_id not in self.scheduled_posts:
                self.scheduled_posts[user_id] = []
            
            self.scheduled_posts[user_id].append(post_data)
            
            return {
                "success": True,
                "post_id": post_id,
                "scheduled_time": scheduled_time,
                "message": "Post scheduled successfully",
                "post_data": post_data
            }
            
        except Exception as e:
            logger.error(f"Post scheduling failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to schedule post"
            }
    
    async def get_optimal_posting_times(
        self,
        user_profile: Dict[str, Any],
        target_audience: str = "professional"
    ) -> List[Dict[str, Any]]:
        """Get optimal posting times based on audience and industry"""
        try:
            logger.info("⏰ Calculating optimal posting times")
            
            # Industry-specific optimal times
            industry_times = {
                "Technology": [
                    {"day": "Tuesday", "time": "09:00", "engagement_score": 85},
                    {"day": "Wednesday", "time": "14:00", "engagement_score": 82},
                    {"day": "Thursday", "time": "10:00", "engagement_score": 80},
                    {"day": "Monday", "time": "08:00", "engagement_score": 75},
                    {"day": "Friday", "time": "15:00", "engagement_score": 70}
                ],
                "Marketing": [
                    {"day": "Tuesday", "time": "11:00", "engagement_score": 88},
                    {"day": "Wednesday", "time": "15:00", "engagement_score": 85},
                    {"day": "Thursday", "time": "09:00", "engagement_score": 83},
                    {"day": "Monday", "time": "10:00", "engagement_score": 78},
                    {"day": "Friday", "time": "14:00", "engagement_score": 72}
                ],
                "Finance": [
                    {"day": "Monday", "time": "07:00", "engagement_score": 87},
                    {"day": "Tuesday", "time": "08:00", "engagement_score": 85},
                    {"day": "Wednesday", "time": "17:00", "engagement_score": 82},
                    {"day": "Thursday", "time": "07:30", "engagement_score": 80},
                    {"day": "Friday", "time": "16:00", "engagement_score": 75}
                ]
            }
            
            industry = user_profile.get("industry", "Technology")
            optimal_times = industry_times.get(industry, industry_times["Technology"])
            
            # Add timezone and next occurrence
            for time_slot in optimal_times:
                time_slot["timezone"] = user_profile.get("timezone", "UTC")
                time_slot["next_occurrence"] = await self._get_next_occurrence(
                    time_slot["day"], 
                    time_slot["time"]
                )
            
            return optimal_times
            
        except Exception as e:
            logger.error(f"Optimal times calculation failed: {e}")
            return [
                {"day": "Tuesday", "time": "09:00", "engagement_score": 80, "timezone": "UTC"},
                {"day": "Wednesday", "time": "14:00", "engagement_score": 78, "timezone": "UTC"},
                {"day": "Thursday", "time": "10:00", "engagement_score": 75, "timezone": "UTC"}
            ]
    
    async def get_content_templates(self, content_type: str = "all") -> List[Dict[str, Any]]:
        """Get content templates for different post types"""
        try:
            templates = {
                "text": [
                    {
                        "id": "industry_insight",
                        "name": "Industry Insight",
                        "template": "🔍 Industry Insight: {topic}\n\n{main_content}\n\nKey takeaways:\n• {point_1}\n• {point_2}\n• {point_3}\n\nWhat's your experience with {topic}? Share your thoughts below! 👇",
                        "variables": ["topic", "main_content", "point_1", "point_2", "point_3"],
                        "category": "thought_leadership"
                    },
                    {
                        "id": "personal_story",
                        "name": "Personal Story",
                        "template": "💡 A lesson I learned: {lesson_title}\n\n{story_content}\n\nThe key insight: {insight}\n\nHave you experienced something similar? I'd love to hear your story! 🤝",
                        "variables": ["lesson_title", "story_content", "insight"],
                        "category": "personal_branding"
                    }
                ],
                "carousel": [
                    {
                        "id": "tips_carousel",
                        "name": "Tips Carousel",
                        "template": "📊 {number} {topic} Tips\n\nSlide 1: {tip_1}\nSlide 2: {tip_2}\nSlide 3: {tip_3}\nSlide 4: {tip_4}\nSlide 5: {tip_5}",
                        "variables": ["number", "topic", "tip_1", "tip_2", "tip_3", "tip_4", "tip_5"],
                        "category": "educational"
                    }
                ],
                "poll": [
                    {
                        "id": "industry_poll",
                        "name": "Industry Poll",
                        "template": "🗳️ Quick poll: {question}\n\n{context}\n\nVote and share your reasoning in the comments!",
                        "variables": ["question", "context"],
                        "category": "engagement"
                    }
                ]
            }
            
            if content_type == "all":
                all_templates = []
                for template_list in templates.values():
                    all_templates.extend(template_list)
                return all_templates
            
            return templates.get(content_type, [])
            
        except Exception as e:
            logger.error(f"Template retrieval failed: {e}")
            return []
    
    async def _get_scheduled_posts(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get scheduled posts in date range"""
        try:
            user_posts = self.scheduled_posts.get(user_id, [])
            
            filtered_posts = []
            for post in user_posts:
                post_date = datetime.fromisoformat(post["scheduled_time"].replace('Z', '+00:00'))
                if start_date <= post_date <= end_date:
                    filtered_posts.append(post)
            
            return sorted(filtered_posts, key=lambda x: x["scheduled_time"])
            
        except Exception as e:
            logger.error(f"Scheduled posts retrieval failed: {e}")
            return []
    
    async def _generate_calendar_data(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        scheduled_posts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate calendar grid data"""
        try:
            calendar_data = []
            current_date = start_date.date()
            end_date_only = end_date.date()
            
            while current_date <= end_date_only:
                # Get posts for this date
                day_posts = [
                    post for post in scheduled_posts
                    if datetime.fromisoformat(post["scheduled_time"].replace('Z', '+00:00')).date() == current_date
                ]
                
                calendar_data.append({
                    "date": current_date.isoformat(),
                    "day_of_week": current_date.strftime("%A"),
                    "posts_count": len(day_posts),
                    "posts": day_posts,
                    "is_optimal": await self._is_optimal_posting_day(current_date),
                    "engagement_forecast": await self._forecast_engagement(current_date, day_posts)
                })
                
                current_date += timedelta(days=1)
            
            return calendar_data
            
        except Exception as e:
            logger.error(f"Calendar data generation failed: {e}")
            return []
    
    async def _get_content_suggestions(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get content suggestions for empty calendar slots"""
        try:
            suggestions = [
                {
                    "type": "industry_trend",
                    "title": "Share an industry trend analysis",
                    "description": "Analyze a current trend in your industry",
                    "estimated_engagement": 75,
                    "optimal_time": "Tuesday 09:00"
                },
                {
                    "type": "personal_insight",
                    "title": "Share a personal professional insight",
                    "description": "Tell a story about a lesson learned",
                    "estimated_engagement": 82,
                    "optimal_time": "Wednesday 14:00"
                },
                {
                    "type": "tips_carousel",
                    "title": "Create a tips carousel",
                    "description": "Share 5 actionable tips in your expertise area",
                    "estimated_engagement": 88,
                    "optimal_time": "Thursday 10:00"
                }
            ]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Content suggestions failed: {e}")
            return []
    
    async def _estimate_engagement(
        self, 
        content: Dict[str, Any], 
        scheduled_time: datetime
    ) -> Dict[str, Any]:
        """Estimate engagement for scheduled content"""
        try:
            # Base engagement score
            base_score = 70
            
            # Time-based multiplier
            hour = scheduled_time.hour
            if 8 <= hour <= 10 or 14 <= hour <= 16:
                time_multiplier = 1.2
            elif 11 <= hour <= 13:
                time_multiplier = 1.1
            else:
                time_multiplier = 0.9
            
            # Day-based multiplier
            weekday = scheduled_time.weekday()
            if weekday in [1, 2, 3]:  # Tuesday, Wednesday, Thursday
                day_multiplier = 1.15
            elif weekday == 0:  # Monday
                day_multiplier = 1.05
            else:  # Friday, Weekend
                day_multiplier = 0.85
            
            # Content type multiplier
            content_type = content.get("type", "text")
            type_multipliers = {
                "carousel": 1.3,
                "video": 1.25,
                "poll": 1.2,
                "text": 1.0,
                "article": 0.9
            }
            
            final_score = int(base_score * time_multiplier * day_multiplier * type_multipliers.get(content_type, 1.0))
            
            return {
                "estimated_likes": final_score * 2,
                "estimated_comments": final_score // 5,
                "estimated_shares": final_score // 10,
                "engagement_score": min(final_score, 100)
            }
            
        except Exception as e:
            logger.error(f"Engagement estimation failed: {e}")
            return {
                "estimated_likes": 50,
                "estimated_comments": 10,
                "estimated_shares": 5,
                "engagement_score": 70
            }
    
    async def _get_next_occurrence(self, day_name: str, time_str: str) -> str:
        """Get next occurrence of a specific day and time"""
        try:
            days = {
                "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                "Friday": 4, "Saturday": 5, "Sunday": 6
            }
            
            target_day = days[day_name]
            current_date = datetime.now().date()
            current_weekday = current_date.weekday()
            
            days_ahead = target_day - current_weekday
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            
            target_date = current_date + timedelta(days=days_ahead)
            target_datetime = datetime.combine(target_date, datetime.strptime(time_str, "%H:%M").time())
            
            return target_datetime.isoformat()
            
        except Exception as e:
            logger.error(f"Next occurrence calculation failed: {e}")
            return datetime.now().isoformat()
    
    async def _is_optimal_posting_day(self, date: date) -> bool:
        """Check if date is optimal for posting"""
        weekday = date.weekday()
        return weekday in [1, 2, 3]  # Tuesday, Wednesday, Thursday
    
    async def _forecast_engagement(
        self, 
        date: date, 
        posts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Forecast engagement for a specific date"""
        try:
            if not posts:
                return {"forecast": "low", "score": 30}
            
            total_score = sum(
                post.get("estimated_engagement", {}).get("engagement_score", 70)
                for post in posts
            )
            avg_score = total_score / len(posts)
            
            if avg_score >= 80:
                forecast = "high"
            elif avg_score >= 60:
                forecast = "medium"
            else:
                forecast = "low"
            
            return {"forecast": forecast, "score": int(avg_score)}
            
        except Exception as e:
            logger.error(f"Engagement forecast failed: {e}")
            return {"forecast": "medium", "score": 60}
    
    async def _get_fallback_calendar(self) -> Dict[str, Any]:
        """Get fallback calendar data"""
        return {
            "calendar_data": [],
            "scheduled_posts": [],
            "content_suggestions": [],
            "total_posts": 0,
            "date_range": {
                "start": datetime.now().isoformat(),
                "end": (datetime.now() + timedelta(days=30)).isoformat()
            },
            "generated_at": datetime.now().isoformat()
        }

# Global service instance
content_calendar = ContentCalendarService()
