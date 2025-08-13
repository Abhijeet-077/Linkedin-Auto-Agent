"""
Open-Source Image Generation Service
Using Hugging Face models for image generation
"""

import asyncio
import os
import json
import aiohttp
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from app.core.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

class OpenSourceImageGenerator:
    """Open-source image generation using Hugging Face models"""
    
    def __init__(self):
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Available models for image generation
        self.models = {
            "stable_diffusion": "runwayml/stable-diffusion-v1-5",
            "stable_diffusion_xl": "stabilityai/stable-diffusion-xl-base-1.0",
            "flux": "black-forest-labs/FLUX.1-schnell",
            "playground": "playgroundai/playground-v2.5-1024px-aesthetic"
        }
        
        # Fallback professional images
        self.fallback_images = {
            "technology": [
                "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=600&fit=crop"
            ],
            "business": [
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop"
            ],
            "professional": [
                "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1486312338219-ce68e2c6b696?w=800&h=600&fit=crop"
            ]
        }
    
    async def generate_image(
        self, 
        topic: str, 
        content_text: str = "",
        style: str = "professional"
    ) -> str:
        """Generate image using open-source models"""
        try:
            logger.info(f"🎨 Generating image for topic: {topic}")
            
            # Create professional prompt
            prompt = await self._create_professional_prompt(topic, content_text, style)
            
            # Try different models in order of preference
            models_to_try = ["flux", "stable_diffusion_xl", "stable_diffusion", "playground"]
            
            for model_key in models_to_try:
                try:
                    image_url = await self._generate_with_model(model_key, prompt)
                    if image_url:
                        logger.info(f"✅ Image generated successfully with {model_key}")
                        return image_url
                except Exception as e:
                    logger.warning(f"Model {model_key} failed: {e}")
                    continue
            
            # If all models fail, use fallback images
            logger.info("🔄 Using fallback professional images")
            return await self._get_fallback_image(topic)
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return await self._get_fallback_image(topic)
    
    async def _create_professional_prompt(
        self, 
        topic: str, 
        content_text: str, 
        style: str
    ) -> str:
        """Create a professional image generation prompt"""
        try:
            # Base professional style
            base_prompt = f"Professional LinkedIn post image about {topic}, "
            
            # Style-specific additions
            style_prompts = {
                "professional": "clean modern business aesthetic, corporate colors, minimalist design, high quality, professional photography style",
                "creative": "creative modern design, vibrant colors, artistic elements, contemporary style, high quality",
                "technical": "technical illustration, clean diagrams, modern tech aesthetic, blue and white colors, professional",
                "inspirational": "motivational design, uplifting colors, modern typography, professional inspiration"
            }
            
            style_addition = style_prompts.get(style, style_prompts["professional"])
            
            # Topic-specific enhancements
            topic_keywords = await self._extract_topic_keywords(topic, content_text)
            
            # Construct final prompt
            prompt = f"{base_prompt}{style_addition}, {topic_keywords}, no text overlay, suitable for social media, 16:9 aspect ratio"
            
            # Ensure prompt is not too long
            if len(prompt) > 200:
                prompt = prompt[:200] + "..."
            
            logger.info(f"Generated prompt: {prompt[:100]}...")
            return prompt
            
        except Exception as e:
            logger.error(f"Prompt creation failed: {e}")
            return f"Professional business image about {topic}, clean modern design, high quality"
    
    async def _extract_topic_keywords(self, topic: str, content_text: str) -> str:
        """Extract relevant keywords from topic and content"""
        try:
            # Common professional keywords by topic
            keyword_map = {
                "ai": "artificial intelligence, technology, innovation, digital transformation",
                "business": "business growth, strategy, leadership, success",
                "marketing": "digital marketing, branding, social media, analytics",
                "leadership": "team leadership, management, professional development",
                "technology": "tech innovation, digital solutions, modern technology",
                "finance": "financial planning, investment, business finance",
                "startup": "entrepreneurship, innovation, business startup, growth"
            }
            
            # Find matching keywords
            topic_lower = topic.lower()
            for key, keywords in keyword_map.items():
                if key in topic_lower:
                    return keywords
            
            # Default professional keywords
            return "business professional, modern workplace, corporate success"
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return "professional business"
    
    async def _generate_with_model(self, model_key: str, prompt: str) -> Optional[str]:
        """Generate image with specific Hugging Face model"""
        try:
            model_name = self.models[model_key]
            url = f"{self.base_url}/{model_name}"
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}" if self.hf_token else "",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "width": 800,
                    "height": 600
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        # Check if response is JSON (error) or binary (image)
                        content_type = response.headers.get('content-type', '')
                        
                        if 'application/json' in content_type:
                            error_data = await response.json()
                            if 'error' in error_data:
                                logger.warning(f"Model {model_key} error: {error_data['error']}")
                                return None
                        
                        # If it's binary data (image)
                        elif 'image' in content_type or response.status == 200:
                            image_data = await response.read()
                            
                            # Convert to base64 data URL
                            base64_image = base64.b64encode(image_data).decode('utf-8')
                            data_url = f"data:image/png;base64,{base64_image}"
                            
                            logger.info(f"✅ Image generated with {model_key}")
                            return data_url
                    
                    else:
                        logger.warning(f"Model {model_key} returned status {response.status}")
                        return None
            
        except asyncio.TimeoutError:
            logger.warning(f"Model {model_key} timed out")
            return None
        except Exception as e:
            logger.error(f"Model {model_key} generation failed: {e}")
            return None
    
    async def _get_fallback_image(self, topic: str) -> str:
        """Get fallback professional image"""
        try:
            # Determine category based on topic
            topic_lower = topic.lower()
            
            if any(word in topic_lower for word in ['ai', 'tech', 'digital', 'innovation', 'software']):
                category = "technology"
            elif any(word in topic_lower for word in ['business', 'strategy', 'growth', 'success']):
                category = "business"
            else:
                category = "professional"
            
            # Get random image from category
            images = self.fallback_images.get(category, self.fallback_images["professional"])
            import random
            selected_image = random.choice(images)
            
            logger.info(f"Using fallback image from {category} category")
            return selected_image
            
        except Exception as e:
            logger.error(f"Fallback image selection failed: {e}")
            # Return a default professional image
            return "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop"
    
    async def generate_multiple_options(
        self, 
        topic: str, 
        content_text: str = "",
        count: int = 3
    ) -> List[str]:
        """Generate multiple image options"""
        try:
            logger.info(f"🎨 Generating {count} image options for: {topic}")
            
            images = []
            styles = ["professional", "creative", "technical"]
            
            # Generate images with different styles
            for i in range(min(count, len(styles))):
                style = styles[i]
                image_url = await self.generate_image(topic, content_text, style)
                if image_url:
                    images.append(image_url)
            
            # Fill remaining slots with fallback images if needed
            while len(images) < count:
                fallback = await self._get_fallback_image(topic)
                if fallback not in images:
                    images.append(fallback)
                else:
                    break
            
            return images[:count]
            
        except Exception as e:
            logger.error(f"Multiple image generation failed: {e}")
            # Return fallback images
            return [await self._get_fallback_image(topic) for _ in range(count)]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health of image generation services"""
        try:
            status = {
                "service": "OpenSourceImageGenerator",
                "status": "healthy",
                "models_available": len(self.models),
                "hf_token_configured": bool(self.hf_token),
                "fallback_images": sum(len(imgs) for imgs in self.fallback_images.values()),
                "timestamp": datetime.now().isoformat()
            }
            
            # Test a simple generation
            try:
                test_image = await self.generate_image("test", "", "professional")
                status["test_generation"] = "success" if test_image else "failed"
            except Exception as e:
                status["test_generation"] = f"failed: {str(e)}"
            
            return status
            
        except Exception as e:
            return {
                "service": "OpenSourceImageGenerator",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Global service instance
image_generator = OpenSourceImageGenerator()
