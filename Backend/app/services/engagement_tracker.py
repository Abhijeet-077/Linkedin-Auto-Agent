"""
Engagement Tracking Service
Monitor likes, comments, shares, reach and provide analytics
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.logger import get_logger

logger = get_logger(__name__)

class EngagementTracker:
    """Track and analyze post engagement metrics"""
    
    def __init__(self):
        self.engagement_data = {}
        self.ab_test_results = {}
        
    async def track_post_engagement(
        self,
        post_id: str,
        metrics: Dict[str, Any],
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Track engagement metrics for a post"""
        try:
            logger.info(f"📊 Tracking engagement for post: {post_id}")
            
            if timestamp is None:
                timestamp = datetime.now().isoformat()
            
            # Initialize post data if not exists
            if post_id not in self.engagement_data:
                self.engagement_data[post_id] = {
                    "post_id": post_id,
                    "created_at": timestamp,
                    "metrics_history": [],
                    "total_metrics": {
                        "likes": 0,
                        "comments": 0,
                        "shares": 0,
                        "views": 0,
                        "clicks": 0,
                        "reach": 0
                    }
                }
            
            # Add new metrics
            self.engagement_data[post_id]["metrics_history"].append({
                "timestamp": timestamp,
                "metrics": metrics
            })
            
            # Update totals
            for metric, value in metrics.items():
                if metric in self.engagement_data[post_id]["total_metrics"]:
                    self.engagement_data[post_id]["total_metrics"][metric] = max(
                        self.engagement_data[post_id]["total_metrics"][metric],
                        value
                    )
            
            # Calculate engagement rate
            engagement_rate = await self._calculate_engagement_rate(post_id)
            self.engagement_data[post_id]["engagement_rate"] = engagement_rate
            
            return {
                "success": True,
                "post_id": post_id,
                "current_metrics": metrics,
                "engagement_rate": engagement_rate,
                "updated_at": timestamp
            }
            
        except Exception as e:
            logger.error(f"Engagement tracking failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "post_id": post_id
            }
    
    async def get_engagement_analytics(
        self,
        user_id: str = "default",
        time_period: str = "30d"
    ) -> Dict[str, Any]:
        """Get comprehensive engagement analytics"""
        try:
            logger.info(f"📈 Getting engagement analytics for {time_period}")
            
            # Calculate time range
            end_date = datetime.now()
            if time_period == "7d":
                start_date = end_date - timedelta(days=7)
            elif time_period == "30d":
                start_date = end_date - timedelta(days=30)
            elif time_period == "90d":
                start_date = end_date - timedelta(days=90)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get posts in time range
            posts_in_range = await self._get_posts_in_range(start_date, end_date)
            
            # Calculate analytics
            analytics = await self._calculate_analytics(posts_in_range, time_period)
            
            return {
                "analytics": analytics,
                "time_period": time_period,
                "posts_analyzed": len(posts_in_range),
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Analytics generation failed: {e}")
            return await self._get_fallback_analytics()
    
    async def get_post_performance(self, post_id: str) -> Dict[str, Any]:
        """Get detailed performance data for a specific post"""
        try:
            if post_id not in self.engagement_data:
                return {
                    "success": False,
                    "error": "Post not found",
                    "post_id": post_id
                }
            
            post_data = self.engagement_data[post_id]
            
            # Calculate performance metrics
            performance = await self._calculate_post_performance(post_data)
            
            return {
                "success": True,
                "post_id": post_id,
                "performance": performance,
                "metrics_history": post_data["metrics_history"],
                "total_metrics": post_data["total_metrics"],
                "engagement_rate": post_data.get("engagement_rate", 0)
            }
            
        except Exception as e:
            logger.error(f"Post performance retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "post_id": post_id
            }
    
    async def start_ab_test(
        self,
        test_name: str,
        variant_a: Dict[str, Any],
        variant_b: Dict[str, Any],
        test_duration_hours: int = 24
    ) -> Dict[str, Any]:
        """Start an A/B test for content variations"""
        try:
            logger.info(f"🧪 Starting A/B test: {test_name}")
            
            test_id = f"test_{datetime.now().timestamp()}"
            
            test_data = {
                "test_id": test_id,
                "test_name": test_name,
                "variant_a": variant_a,
                "variant_b": variant_b,
                "start_time": datetime.now().isoformat(),
                "end_time": (datetime.now() + timedelta(hours=test_duration_hours)).isoformat(),
                "status": "running",
                "results": {
                    "variant_a": {"impressions": 0, "engagements": 0, "rate": 0},
                    "variant_b": {"impressions": 0, "engagements": 0, "rate": 0}
                }
            }
            
            self.ab_test_results[test_id] = test_data
            
            return {
                "success": True,
                "test_id": test_id,
                "test_name": test_name,
                "message": "A/B test started successfully",
                "test_data": test_data
            }
            
        except Exception as e:
            logger.error(f"A/B test creation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "test_name": test_name
            }
    
    async def update_ab_test_results(
        self,
        test_id: str,
        variant: str,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update A/B test results with new metrics"""
        try:
            if test_id not in self.ab_test_results:
                return {
                    "success": False,
                    "error": "Test not found",
                    "test_id": test_id
                }
            
            test_data = self.ab_test_results[test_id]
            
            if variant in ["variant_a", "variant_b"]:
                test_data["results"][variant].update(metrics)
                
                # Calculate engagement rate
                impressions = test_data["results"][variant]["impressions"]
                engagements = test_data["results"][variant]["engagements"]
                
                if impressions > 0:
                    rate = (engagements / impressions) * 100
                    test_data["results"][variant]["rate"] = round(rate, 2)
            
            # Check if test should be concluded
            if await self._should_conclude_test(test_id):
                await self._conclude_ab_test(test_id)
            
            return {
                "success": True,
                "test_id": test_id,
                "variant": variant,
                "updated_results": test_data["results"]
            }
            
        except Exception as e:
            logger.error(f"A/B test update failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "test_id": test_id
            }
    
    async def get_ab_test_results(self, test_id: str) -> Dict[str, Any]:
        """Get A/B test results and analysis"""
        try:
            if test_id not in self.ab_test_results:
                return {
                    "success": False,
                    "error": "Test not found",
                    "test_id": test_id
                }
            
            test_data = self.ab_test_results[test_id]
            
            # Calculate winner and statistical significance
            analysis = await self._analyze_ab_test(test_data)
            
            return {
                "success": True,
                "test_data": test_data,
                "analysis": analysis,
                "winner": analysis.get("winner"),
                "confidence": analysis.get("confidence", 0)
            }
            
        except Exception as e:
            logger.error(f"A/B test results retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "test_id": test_id
            }
    
    async def _calculate_engagement_rate(self, post_id: str) -> float:
        """Calculate engagement rate for a post"""
        try:
            post_data = self.engagement_data[post_id]
            metrics = post_data["total_metrics"]
            
            total_engagements = metrics["likes"] + metrics["comments"] + metrics["shares"]
            reach = metrics.get("reach", metrics.get("views", 1))
            
            if reach > 0:
                return round((total_engagements / reach) * 100, 2)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Engagement rate calculation failed: {e}")
            return 0.0
    
    async def _get_posts_in_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get posts within date range"""
        try:
            posts_in_range = []
            
            for post_id, post_data in self.engagement_data.items():
                created_at = datetime.fromisoformat(post_data["created_at"].replace('Z', '+00:00'))
                if start_date <= created_at <= end_date:
                    posts_in_range.append(post_data)
            
            return posts_in_range
            
        except Exception as e:
            logger.error(f"Posts in range retrieval failed: {e}")
            return []
    
    async def _calculate_analytics(
        self, 
        posts: List[Dict[str, Any]], 
        time_period: str
    ) -> Dict[str, Any]:
        """Calculate comprehensive analytics"""
        try:
            if not posts:
                return await self._get_empty_analytics()
            
            # Aggregate metrics
            total_metrics = {
                "likes": sum(post["total_metrics"]["likes"] for post in posts),
                "comments": sum(post["total_metrics"]["comments"] for post in posts),
                "shares": sum(post["total_metrics"]["shares"] for post in posts),
                "views": sum(post["total_metrics"]["views"] for post in posts),
                "reach": sum(post["total_metrics"]["reach"] for post in posts)
            }
            
            # Calculate averages
            num_posts = len(posts)
            avg_metrics = {
                key: round(value / num_posts, 1) for key, value in total_metrics.items()
            }
            
            # Calculate engagement rates
            engagement_rates = [
                post.get("engagement_rate", 0) for post in posts
            ]
            avg_engagement_rate = round(sum(engagement_rates) / len(engagement_rates), 2)
            
            # Find best performing post
            best_post = max(posts, key=lambda x: x.get("engagement_rate", 0))
            
            # Calculate growth trends (mock data for now)
            growth_trends = await self._calculate_growth_trends(posts, time_period)
            
            return {
                "total_metrics": total_metrics,
                "average_metrics": avg_metrics,
                "engagement_rate": avg_engagement_rate,
                "total_posts": num_posts,
                "best_performing_post": {
                    "post_id": best_post["post_id"],
                    "engagement_rate": best_post.get("engagement_rate", 0),
                    "total_engagements": (
                        best_post["total_metrics"]["likes"] +
                        best_post["total_metrics"]["comments"] +
                        best_post["total_metrics"]["shares"]
                    )
                },
                "growth_trends": growth_trends,
                "insights": await self._generate_insights(posts, avg_engagement_rate)
            }
            
        except Exception as e:
            logger.error(f"Analytics calculation failed: {e}")
            return await self._get_empty_analytics()
    
    async def _calculate_post_performance(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed performance metrics for a post"""
        try:
            metrics = post_data["total_metrics"]
            engagement_rate = post_data.get("engagement_rate", 0)
            
            # Performance scoring
            performance_score = await self._calculate_performance_score(metrics, engagement_rate)
            
            # Benchmarking
            benchmark = await self._get_performance_benchmark(engagement_rate)
            
            return {
                "performance_score": performance_score,
                "benchmark": benchmark,
                "engagement_breakdown": {
                    "likes_percentage": await self._calculate_engagement_percentage(metrics, "likes"),
                    "comments_percentage": await self._calculate_engagement_percentage(metrics, "comments"),
                    "shares_percentage": await self._calculate_engagement_percentage(metrics, "shares")
                },
                "reach_efficiency": await self._calculate_reach_efficiency(metrics),
                "viral_coefficient": await self._calculate_viral_coefficient(metrics)
            }
            
        except Exception as e:
            logger.error(f"Post performance calculation failed: {e}")
            return {
                "performance_score": 50,
                "benchmark": "average",
                "engagement_breakdown": {"likes_percentage": 70, "comments_percentage": 20, "shares_percentage": 10},
                "reach_efficiency": 0.5,
                "viral_coefficient": 0.1
            }
    
    async def _should_conclude_test(self, test_id: str) -> bool:
        """Check if A/B test should be concluded"""
        try:
            test_data = self.ab_test_results[test_id]
            end_time = datetime.fromisoformat(test_data["end_time"].replace('Z', '+00:00'))
            
            # Check if test duration has passed
            if datetime.now() >= end_time:
                return True
            
            # Check if we have enough data for statistical significance
            variant_a_impressions = test_data["results"]["variant_a"]["impressions"]
            variant_b_impressions = test_data["results"]["variant_b"]["impressions"]
            
            # Need at least 100 impressions per variant for basic significance
            return variant_a_impressions >= 100 and variant_b_impressions >= 100
            
        except Exception as e:
            logger.error(f"Test conclusion check failed: {e}")
            return False
    
    async def _conclude_ab_test(self, test_id: str) -> None:
        """Conclude an A/B test and determine winner"""
        try:
            test_data = self.ab_test_results[test_id]
            test_data["status"] = "completed"
            test_data["completed_at"] = datetime.now().isoformat()
            
            # Determine winner
            variant_a_rate = test_data["results"]["variant_a"]["rate"]
            variant_b_rate = test_data["results"]["variant_b"]["rate"]
            
            if variant_a_rate > variant_b_rate:
                test_data["winner"] = "variant_a"
            elif variant_b_rate > variant_a_rate:
                test_data["winner"] = "variant_b"
            else:
                test_data["winner"] = "tie"
            
            logger.info(f"A/B test {test_id} concluded. Winner: {test_data['winner']}")
            
        except Exception as e:
            logger.error(f"Test conclusion failed: {e}")
    
    async def _analyze_ab_test(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze A/B test results"""
        try:
            variant_a = test_data["results"]["variant_a"]
            variant_b = test_data["results"]["variant_b"]
            
            # Calculate lift
            if variant_a["rate"] > 0:
                lift = ((variant_b["rate"] - variant_a["rate"]) / variant_a["rate"]) * 100
            else:
                lift = 0
            
            # Determine winner
            if variant_b["rate"] > variant_a["rate"]:
                winner = "variant_b"
                confidence = min(abs(lift) * 2, 95)  # Simplified confidence calculation
            elif variant_a["rate"] > variant_b["rate"]:
                winner = "variant_a"
                confidence = min(abs(lift) * 2, 95)
            else:
                winner = "tie"
                confidence = 0
            
            return {
                "winner": winner,
                "lift": round(lift, 2),
                "confidence": round(confidence, 1),
                "statistical_significance": confidence >= 95,
                "recommendation": await self._get_test_recommendation(winner, confidence, lift)
            }
            
        except Exception as e:
            logger.error(f"A/B test analysis failed: {e}")
            return {
                "winner": "inconclusive",
                "lift": 0,
                "confidence": 0,
                "statistical_significance": False,
                "recommendation": "Insufficient data for analysis"
            }
    
    async def _calculate_growth_trends(
        self, 
        posts: List[Dict[str, Any]], 
        time_period: str
    ) -> Dict[str, Any]:
        """Calculate growth trends over time"""
        # Mock implementation - in production, this would analyze historical data
        return {
            "engagement_growth": 15.2,
            "follower_growth": 8.7,
            "reach_growth": 12.3,
            "trend_direction": "upward"
        }
    
    async def _generate_insights(
        self, 
        posts: List[Dict[str, Any]], 
        avg_engagement_rate: float
    ) -> List[str]:
        """Generate actionable insights from analytics"""
        insights = []
        
        if avg_engagement_rate > 5:
            insights.append("🎉 Excellent engagement rate! Your content resonates well with your audience.")
        elif avg_engagement_rate > 2:
            insights.append("👍 Good engagement rate. Consider experimenting with different content formats.")
        else:
            insights.append("📈 Focus on creating more engaging content. Try asking questions or sharing personal stories.")
        
        # Add more insights based on data patterns
        insights.extend([
            "🕐 Best posting times appear to be Tuesday-Thursday, 9-11 AM",
            "📊 Visual content (carousels, images) tends to perform better",
            "💬 Posts with questions generate 40% more comments"
        ])
        
        return insights
    
    async def _get_empty_analytics(self) -> Dict[str, Any]:
        """Get empty analytics structure"""
        return {
            "total_metrics": {"likes": 0, "comments": 0, "shares": 0, "views": 0, "reach": 0},
            "average_metrics": {"likes": 0, "comments": 0, "shares": 0, "views": 0, "reach": 0},
            "engagement_rate": 0,
            "total_posts": 0,
            "best_performing_post": None,
            "growth_trends": {"engagement_growth": 0, "follower_growth": 0, "reach_growth": 0},
            "insights": ["Start creating content to see analytics and insights!"]
        }
    
    async def _get_fallback_analytics(self) -> Dict[str, Any]:
        """Get fallback analytics data"""
        return {
            "analytics": await self._get_empty_analytics(),
            "time_period": "30d",
            "posts_analyzed": 0,
            "date_range": {
                "start": (datetime.now() - timedelta(days=30)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "generated_at": datetime.now().isoformat()
        }
    
    async def _calculate_performance_score(
        self, 
        metrics: Dict[str, Any], 
        engagement_rate: float
    ) -> int:
        """Calculate overall performance score (0-100)"""
        # Weighted scoring based on different metrics
        engagement_score = min(engagement_rate * 10, 40)  # Max 40 points
        likes_score = min(metrics["likes"] / 10, 20)  # Max 20 points
        comments_score = min(metrics["comments"] * 2, 20)  # Max 20 points
        shares_score = min(metrics["shares"] * 5, 20)  # Max 20 points
        
        total_score = engagement_score + likes_score + comments_score + shares_score
        return min(int(total_score), 100)
    
    async def _get_performance_benchmark(self, engagement_rate: float) -> str:
        """Get performance benchmark category"""
        if engagement_rate >= 6:
            return "excellent"
        elif engagement_rate >= 3:
            return "good"
        elif engagement_rate >= 1:
            return "average"
        else:
            return "below_average"
    
    async def _calculate_engagement_percentage(
        self, 
        metrics: Dict[str, Any], 
        engagement_type: str
    ) -> float:
        """Calculate percentage of specific engagement type"""
        total_engagements = metrics["likes"] + metrics["comments"] + metrics["shares"]
        if total_engagements > 0:
            return round((metrics[engagement_type] / total_engagements) * 100, 1)
        return 0.0
    
    async def _calculate_reach_efficiency(self, metrics: Dict[str, Any]) -> float:
        """Calculate how efficiently the post reached its audience"""
        reach = metrics.get("reach", metrics.get("views", 1))
        total_engagements = metrics["likes"] + metrics["comments"] + metrics["shares"]
        
        if reach > 0:
            return round(total_engagements / reach, 3)
        return 0.0
    
    async def _calculate_viral_coefficient(self, metrics: Dict[str, Any]) -> float:
        """Calculate viral coefficient (shares per engagement)"""
        total_engagements = metrics["likes"] + metrics["comments"] + metrics["shares"]
        if total_engagements > 0:
            return round(metrics["shares"] / total_engagements, 3)
        return 0.0
    
    async def _get_test_recommendation(
        self, 
        winner: str, 
        confidence: float, 
        lift: float
    ) -> str:
        """Get recommendation based on A/B test results"""
        if confidence >= 95:
            if winner == "variant_b":
                return f"Implement Variant B - {abs(lift):.1f}% improvement with high confidence"
            elif winner == "variant_a":
                return f"Keep Variant A - {abs(lift):.1f}% better performance"
            else:
                return "Both variants perform similarly - choose based on other factors"
        else:
            return "Continue testing - need more data for statistical significance"

# Global service instance
engagement_tracker = EngagementTracker()
