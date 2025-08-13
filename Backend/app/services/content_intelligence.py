"""
Intelligent Content Creation Service
Advanced AI-powered content generation with industry analysis and trend research
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.logger import get_logger

logger = get_logger(__name__)

# Import model_manager with fallback
try:
    from app.services.model_manager import model_manager
    MODEL_MANAGER_AVAILABLE = True
except ImportError:
    MODEL_MANAGER_AVAILABLE = False
    model_manager = None

class ContentIntelligenceService:
    """Advanced content intelligence and generation service"""
    
    def __init__(self):
        self.trend_cache = {}
        self.industry_data = {}
        
    async def generate_intelligent_content(
        self, 
        topic: str, 
        user_profile: Dict[str, Any],
        content_type: str = "text",
        target_audience: str = "professional"
    ) -> Dict[str, Any]:
        """Generate intelligent content based on user profile and trends"""
        try:
            logger.info(f"🧠 Generating intelligent content for: {topic}")
            
            # Analyze user profile and industry
            industry_context = await self._analyze_industry_context(
                user_profile.get("industry", "Technology"),
                user_profile.get("role", "Professional")
            )
            
            # Research current trends
            trends = await self._research_trends(
                user_profile.get("industry", "Technology"),
                topic
            )
            
            # Generate content with context
            content = await self._generate_contextual_content(
                topic=topic,
                user_profile=user_profile,
                industry_context=industry_context,
                trends=trends,
                content_type=content_type,
                target_audience=target_audience
            )
            
            # Optimize hashtags
            hashtags = await self._optimize_hashtags(
                content["text"],
                user_profile.get("industry", "Technology"),
                trends
            )
            
            # Generate brand voice consistent content
            content["text"] = await self._apply_brand_voice(
                content["text"],
                user_profile.get("brand_voice", "professional")
            )
            
            return {
                **content,
                "hashtags": hashtags,
                "trends_incorporated": trends[:3],
                "industry_context": industry_context,
                "content_type": content_type,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content intelligence generation failed: {e}")
            # Fallback to basic generation
            if MODEL_MANAGER_AVAILABLE and model_manager:
                return await model_manager.generate_content(topic)
            else:
                return {
                    "text": f"Professional insight about {topic}. This is a sample post generated for demonstration purposes.",
                    "hashtags": ["#LinkedIn", "#Professional", "#Growth", "#Innovation"],
                    "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop"
                }
    
    async def _analyze_industry_context(self, industry: str, role: str) -> Dict[str, Any]:
        """Analyze industry context and current landscape"""
        try:
            # Industry-specific insights
            industry_insights = {
                "Technology": {
                    "key_topics": ["AI", "Machine Learning", "Cloud Computing", "Cybersecurity", "DevOps"],
                    "trending_keywords": ["automation", "digital transformation", "innovation"],
                    "audience_interests": ["technical solutions", "industry trends", "best practices"]
                },
                "Marketing": {
                    "key_topics": ["Digital Marketing", "Content Strategy", "SEO", "Social Media", "Analytics"],
                    "trending_keywords": ["personalization", "customer experience", "data-driven"],
                    "audience_interests": ["marketing strategies", "campaign results", "industry insights"]
                },
                "Finance": {
                    "key_topics": ["FinTech", "Investment", "Risk Management", "Blockchain", "RegTech"],
                    "trending_keywords": ["digital banking", "cryptocurrency", "financial planning"],
                    "audience_interests": ["market analysis", "investment strategies", "financial advice"]
                },
                "Healthcare": {
                    "key_topics": ["Digital Health", "Telemedicine", "Medical Technology", "Patient Care"],
                    "trending_keywords": ["healthcare innovation", "patient outcomes", "medical research"],
                    "audience_interests": ["healthcare trends", "medical breakthroughs", "patient care"]
                }
            }
            
            context = industry_insights.get(industry, industry_insights["Technology"])
            context["industry"] = industry
            context["role"] = role
            context["analysis_date"] = datetime.now().isoformat()
            
            return context
            
        except Exception as e:
            logger.error(f"Industry analysis failed: {e}")
            return {
                "industry": industry,
                "role": role,
                "key_topics": ["Professional Development", "Industry Trends"],
                "trending_keywords": ["innovation", "growth", "success"],
                "audience_interests": ["professional insights", "industry news"]
            }
    
    async def _research_trends(self, industry: str, topic: str) -> List[str]:
        """Research current industry trends"""
        try:
            # Check cache first
            cache_key = f"{industry}_{topic}"
            if cache_key in self.trend_cache:
                cached_data = self.trend_cache[cache_key]
                if datetime.now() - cached_data["timestamp"] < timedelta(hours=6):
                    return cached_data["trends"]
            
            # Simulate trend research (in production, this would call real APIs)
            trends = await self._simulate_trend_research(industry, topic)
            
            # Cache results
            self.trend_cache[cache_key] = {
                "trends": trends,
                "timestamp": datetime.now()
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Trend research failed: {e}")
            return ["innovation", "digital transformation", "growth", "leadership"]
    
    async def _simulate_trend_research(self, industry: str, topic: str) -> List[str]:
        """Simulate trend research (replace with real API calls in production)"""
        industry_trends = {
            "Technology": [
                "artificial intelligence adoption",
                "cloud-first strategies", 
                "cybersecurity awareness",
                "remote work technologies",
                "sustainable tech solutions",
                "edge computing growth",
                "quantum computing research"
            ],
            "Marketing": [
                "personalized customer experiences",
                "video content dominance",
                "influencer partnerships",
                "voice search optimization",
                "privacy-first marketing",
                "omnichannel strategies",
                "AI-powered analytics"
            ],
            "Finance": [
                "digital banking transformation",
                "cryptocurrency adoption",
                "ESG investing growth",
                "robo-advisor popularity",
                "open banking initiatives",
                "regulatory technology",
                "financial wellness focus"
            ]
        }
        
        base_trends = industry_trends.get(industry, industry_trends["Technology"])
        
        # Filter trends relevant to topic
        relevant_trends = [
            trend for trend in base_trends 
            if any(word in trend.lower() for word in topic.lower().split())
        ]
        
        # If no relevant trends, return top general trends
        if not relevant_trends:
            relevant_trends = base_trends[:5]
        
        return relevant_trends[:7]
    
    async def _generate_contextual_content(
        self,
        topic: str,
        user_profile: Dict[str, Any],
        industry_context: Dict[str, Any],
        trends: List[str],
        content_type: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Generate content with full context"""
        try:
            # Create enhanced prompt with context
            context_prompt = f"""Create a {content_type} LinkedIn post about: {topic}

User Profile Context:
- Industry: {user_profile.get('industry', 'Technology')}
- Role: {user_profile.get('role', 'Professional')}
- Experience Level: {user_profile.get('experience_level', 'Mid-level')}
- Interests: {', '.join(user_profile.get('interests', ['Professional Development']))}

Industry Context:
- Key Topics: {', '.join(industry_context.get('key_topics', []))}
- Trending Keywords: {', '.join(industry_context.get('trending_keywords', []))}

Current Trends to Incorporate:
{chr(10).join(f'- {trend}' for trend in trends[:3])}

Content Requirements:
- Target Audience: {target_audience}
- Tone: Professional yet engaging
- Length: 150-300 words
- Include relevant industry insights
- Incorporate 1-2 current trends naturally
- Add a compelling call-to-action
- Use emojis sparingly but effectively
- No hashtags (will be generated separately)

Create content that demonstrates thought leadership and provides genuine value to the audience."""

            # Generate content using the model manager
            if MODEL_MANAGER_AVAILABLE and model_manager:
                content_data = await model_manager.generate_content(context_prompt)
                return content_data
            else:
                # Mock content generation
                return {
                    "text": f"Professional insight about {topic}. This content demonstrates thought leadership and provides genuine value to the audience.",
                    "hashtags": ["#LinkedIn", "#Professional", "#Growth"],
                    "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop"
                }

        except Exception as e:
            logger.error(f"Contextual content generation failed: {e}")
            # Fallback to basic generation
            if MODEL_MANAGER_AVAILABLE and model_manager:
                return await model_manager.generate_content(topic)
            else:
                return {
                    "text": f"Professional insight about {topic}. This is a sample post generated for demonstration purposes.",
                    "hashtags": ["#LinkedIn", "#Professional", "#Growth"],
                    "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop"
                }
    
    async def _optimize_hashtags(
        self, 
        content: str, 
        industry: str, 
        trends: List[str]
    ) -> List[str]:
        """Optimize hashtags based on content, industry, and trends"""
        try:
            # Industry-specific hashtag pools
            industry_hashtags = {
                "Technology": [
                    "#Technology", "#Innovation", "#AI", "#MachineLearning", 
                    "#CloudComputing", "#Cybersecurity", "#DevOps", "#TechTrends",
                    "#DigitalTransformation", "#Automation", "#SoftwareDevelopment"
                ],
                "Marketing": [
                    "#Marketing", "#DigitalMarketing", "#ContentMarketing", "#SEO",
                    "#SocialMediaMarketing", "#MarketingStrategy", "#BrandBuilding",
                    "#CustomerExperience", "#MarketingTips", "#GrowthHacking"
                ],
                "Finance": [
                    "#Finance", "#FinTech", "#Investment", "#Banking", "#Cryptocurrency",
                    "#FinancialPlanning", "#WealthManagement", "#RiskManagement",
                    "#FinancialTechnology", "#PersonalFinance"
                ]
            }
            
            # Get base hashtags for industry
            base_hashtags = industry_hashtags.get(industry, industry_hashtags["Technology"])
            
            # Add trend-based hashtags
            trend_hashtags = []
            for trend in trends[:2]:
                # Convert trend to hashtag format
                hashtag = "#" + "".join(word.capitalize() for word in trend.split()[:2])
                if len(hashtag) <= 20:  # Keep hashtags reasonable length
                    trend_hashtags.append(hashtag)
            
            # Combine and select best hashtags
            all_hashtags = base_hashtags + trend_hashtags + [
                "#LinkedIn", "#Professional", "#Leadership", "#Growth", "#Success"
            ]
            
            # Remove duplicates and select top 8
            unique_hashtags = list(dict.fromkeys(all_hashtags))
            return unique_hashtags[:8]
            
        except Exception as e:
            logger.error(f"Hashtag optimization failed: {e}")
            return ["#LinkedIn", "#Professional", "#Industry", "#Growth", "#Innovation"]
    
    async def _apply_brand_voice(self, content: str, brand_voice: str) -> str:
        """Apply consistent brand voice to content"""
        try:
            voice_styles = {
                "professional": "formal, authoritative, industry-focused",
                "friendly": "approachable, conversational, warm",
                "innovative": "forward-thinking, creative, trend-setting",
                "educational": "informative, helpful, teaching-oriented",
                "inspirational": "motivating, uplifting, encouraging"
            }
            
            style = voice_styles.get(brand_voice, voice_styles["professional"])
            
            # In a real implementation, this would use AI to adjust tone
            # For now, return content as-is since it's already generated with context
            return content
            
        except Exception as e:
            logger.error(f"Brand voice application failed: {e}")
            return content

# Global service instance
content_intelligence = ContentIntelligenceService()
