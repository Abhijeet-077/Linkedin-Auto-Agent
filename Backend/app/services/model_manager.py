"""
AI Model Management Service
Enhanced with multiple AI providers and model switching
"""
import asyncio
import os
import json
from typing import Optional, Dict, Any, List, Union
from dotenv import load_dotenv
from app.core.config import settings
from app.core.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

try:
    from app.services.rag_pipeline import rag_pipeline
    RAG_AVAILABLE = True
except ImportError as e:
    RAG_AVAILABLE = False
    logger.warning(f"RAG pipeline not available: {e}")
    rag_pipeline = None

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available - install with: pip install openai")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available - install with: pip install transformers torch")

try:
    from PIL import Image
    import requests
    import aiohttp
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False
    logger.warning("Image processing not available - install with: pip install Pillow requests aiohttp")

# OpenRouter API configuration (from environment variables)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Validate required environment variables
if not OPENROUTER_API_KEY:
    logger.warning("⚠️ OPENROUTER_API_KEY not found in environment variables")
    logger.warning("   Please set OPENROUTER_API_KEY in your .env file")
else:
    logger.info("✅ OpenRouter API key loaded from environment")

# Local model configurations
LOCAL_MODELS = {
    "mistral-7b": {
        "model_name": "mistralai/Mistral-7B-Instruct-v0.1",
        "max_length": 2048,
        "temperature": 0.7
    },
    "qwen": {
        "model_name": "Qwen/Qwen-7B-Chat",
        "max_length": 2048,
        "temperature": 0.7
    }
}

class ModelManager:
    """Enhanced AI Model Manager with local LLMs and OpenRouter support"""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.local_models: Dict[str, Any] = {}
        self.loaded = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu" if TRANSFORMERS_AVAILABLE else None
    
    async def load_models(self) -> None:
        """Load AI models including local LLMs and OpenRouter"""
        try:
            logger.info("🤖 Loading AI models...")

            # Initialize RAG pipeline
            if RAG_AVAILABLE:
                await rag_pipeline.initialize()
                self.models['rag'] = True
                logger.info("✅ RAG pipeline initialized")

            # Load local models (Mistral 7B, Qwen)
            if TRANSFORMERS_AVAILABLE:
                await self._load_local_models()

            # OpenRouter API (always available with provided key)
            self.models['openrouter'] = True
            logger.info("✅ OpenRouter API configured")

            # OpenAI API (if available)
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                self.models['openai'] = True
                logger.info("✅ OpenAI API available")

            self.loaded = True
            logger.info("✅ AI models loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            # Fallback to OpenRouter (always available)
            self.models = {'openrouter': True}
            self.loaded = True

    async def _load_local_models(self) -> None:
        """Load local LLM models (Mistral 7B, Qwen)"""
        try:
            logger.info(f"🔧 Loading local models on device: {self.device}")

            # Try to load Mistral 7B first (smaller, faster)
            try:
                logger.info("📥 Loading Mistral 7B model...")
                mistral_config = LOCAL_MODELS["mistral-7b"]

                tokenizer = AutoTokenizer.from_pretrained(mistral_config["model_name"])
                model = AutoModelForCausalLM.from_pretrained(
                    mistral_config["model_name"],
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    low_cpu_mem_usage=True
                )

                self.local_models["mistral-7b"] = {
                    "tokenizer": tokenizer,
                    "model": model,
                    "config": mistral_config
                }
                self.models['mistral-7b'] = True
                logger.info("✅ Mistral 7B loaded successfully")

            except Exception as e:
                logger.warning(f"⚠️ Failed to load Mistral 7B: {e}")

            # Try to load Qwen if Mistral failed or as backup
            try:
                logger.info("📥 Loading Qwen model...")
                qwen_config = LOCAL_MODELS["qwen"]

                tokenizer = AutoTokenizer.from_pretrained(qwen_config["model_name"])
                model = AutoModelForCausalLM.from_pretrained(
                    qwen_config["model_name"],
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    low_cpu_mem_usage=True
                )

                self.local_models["qwen"] = {
                    "tokenizer": tokenizer,
                    "model": model,
                    "config": qwen_config
                }
                self.models['qwen'] = True
                logger.info("✅ Qwen model loaded successfully")

            except Exception as e:
                logger.warning(f"⚠️ Failed to load Qwen: {e}")

            if not self.local_models:
                logger.warning("⚠️ No local models loaded, will use OpenRouter API")

        except Exception as e:
            logger.error(f"❌ Failed to load local models: {e}")
    
    async def generate_content(self, topic: str) -> Dict[str, Any]:
        """Generate LinkedIn content using best available model"""
        if not self.loaded:
            await self.load_models()

        try:
            # Priority order: Local models -> OpenRouter -> OpenAI -> Mock

            # Try local models first (free and fast)
            if self.local_models:
                if 'mistral-7b' in self.local_models:
                    return await self._generate_with_local_model(topic, 'mistral-7b')
                elif 'qwen' in self.local_models:
                    return await self._generate_with_local_model(topic, 'qwen')

            # Fallback to OpenRouter API
            if 'openrouter' in self.models:
                return await self._generate_with_openrouter(topic)

            # Fallback to OpenAI if available
            if 'openai' in self.models and hasattr(settings, 'OPENAI_API_KEY'):
                return await self._generate_with_openai(topic)

            # Final fallback to mock
            return await self._generate_mock_content(topic)

        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            # Try OpenRouter as backup
            try:
                return await self._generate_with_openrouter(topic)
            except:
                return await self._generate_mock_content(topic)

    async def _generate_with_local_model(self, topic: str, model_name: str) -> Dict[str, Any]:
        """Generate content using local LLM model"""
        try:
            logger.info(f"🤖 Generating content with {model_name}")

            model_data = self.local_models[model_name]
            tokenizer = model_data["tokenizer"]
            model = model_data["model"]
            config = model_data["config"]

            # Create prompt for LinkedIn content generation
            prompt = f"""Create a professional LinkedIn post about: {topic}

Requirements:
- Professional and engaging tone
- 150-300 words
- Include relevant insights and value
- Add a call to action
- Use emojis sparingly but effectively
- No hashtags (they will be generated separately)

LinkedIn Post:"""

            # Tokenize and generate
            inputs = tokenizer.encode(prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = inputs.to("cuda")

            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=inputs.shape[1] + config["max_length"],
                    temperature=config["temperature"],
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    num_return_sequences=1
                )

            # Decode the generated text
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            content_text = generated_text[len(prompt):].strip()

            # Generate hashtags using the same model
            hashtag_prompt = f"Generate 5-8 relevant professional hashtags for this LinkedIn post topic: {topic}\nHashtags:"
            hashtag_inputs = tokenizer.encode(hashtag_prompt, return_tensors="pt")
            if self.device == "cuda":
                hashtag_inputs = hashtag_inputs.to("cuda")

            with torch.no_grad():
                hashtag_outputs = model.generate(
                    hashtag_inputs,
                    max_length=hashtag_inputs.shape[1] + 100,
                    temperature=0.5,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )

            hashtag_text = tokenizer.decode(hashtag_outputs[0], skip_special_tokens=True)
            hashtag_content = hashtag_text[len(hashtag_prompt):].strip()

            # Parse hashtags
            hashtags = []
            for line in hashtag_content.split('\n'):
                if line.strip().startswith('#'):
                    hashtags.extend([tag.strip() for tag in line.split() if tag.startswith('#')])

            if not hashtags:
                hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth"]

            # Generate image using OpenRouter API
            image_url = await self._generate_image_with_openrouter(topic, content_text)

            return {
                "text": content_text,
                "hashtags": hashtags[:8],  # Limit to 8 hashtags
                "image_url": image_url,
                "model_used": model_name
            }

        except Exception as e:
            logger.error(f"Local model generation failed: {e}")
            raise

    async def _generate_with_openrouter(self, topic: str) -> Dict[str, Any]:
        """Generate content using OpenRouter API"""
        try:
            if not OPENROUTER_API_KEY:
                raise ValueError("OpenRouter API key not configured")

            logger.info("🌐 Generating content with OpenRouter API")

            async with aiohttp.ClientSession() as session:
                # Generate main content
                content_prompt = f"""Create a professional LinkedIn post about: {topic}

Requirements:
- Professional and engaging tone
- 150-300 words
- Include relevant insights and value
- Add a call to action
- Use emojis sparingly but effectively
- No hashtags (they will be generated separately)

LinkedIn Post:"""

                async with session.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [{"role": "user", "content": content_prompt}],
                        "max_tokens": 500,
                        "temperature": 0.7
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content_text = data["choices"][0]["message"]["content"].strip()
                    else:
                        raise Exception(f"OpenRouter API error: {response.status}")

                # Generate hashtags
                hashtag_prompt = f"Generate 5-8 relevant professional hashtags for this LinkedIn post topic: {topic}. Return only hashtags with # symbol, separated by spaces."

                async with session.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [{"role": "user", "content": hashtag_prompt}],
                        "max_tokens": 100,
                        "temperature": 0.5
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        hashtag_text = data["choices"][0]["message"]["content"].strip()
                        hashtags = [tag.strip() for tag in hashtag_text.split() if tag.startswith('#')]
                    else:
                        hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth"]

                # Generate image using OpenRouter API
                image_url = await self._generate_image_with_openrouter(topic, content_text)

                return {
                    "text": content_text,
                    "hashtags": hashtags[:8],
                    "image_url": image_url,
                    "model_used": "openrouter-mistral"
                }

        except Exception as e:
            logger.error(f"OpenRouter generation failed: {e}")
            raise

    async def _generate_image_with_openrouter(self, topic: str, content_text: str) -> str:
        """Generate image using OpenRouter API with DALL-E or similar model"""
        try:
            if not OPENROUTER_API_KEY:
                logger.warning("OpenRouter API key not configured, using placeholder image")
                return await self._generate_placeholder_image(topic)

            logger.info("🎨 Generating image with OpenRouter API")

            # Create a descriptive prompt for image generation
            image_prompt = f"""Create a professional, modern LinkedIn post image for: {topic}

Style requirements:
- Professional and clean design
- Modern business aesthetic
- Suitable for LinkedIn social media
- High quality and engaging
- Related to: {topic}
- Colors: Professional blues, whites, or corporate colors
- Include subtle tech/business elements if relevant

The image should complement this content: {content_text[:100]}..."""

            async with aiohttp.ClientSession() as session:
                # Try DALL-E 3 first (best quality)
                try:
                    async with session.post(
                        f"{OPENROUTER_BASE_URL}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "openai/dall-e-3",
                            "messages": [{"role": "user", "content": f"Generate an image: {image_prompt}"}],
                            "max_tokens": 1000
                        }
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Extract image URL from response
                            if "choices" in data and len(data["choices"]) > 0:
                                image_content = data["choices"][0]["message"]["content"]
                                # Look for image URL in the response
                                if "http" in image_content:
                                    import re
                                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', image_content)
                                    if urls:
                                        logger.info("✅ Image generated successfully with DALL-E 3")
                                        return urls[0]
                except Exception as e:
                    logger.warning(f"DALL-E 3 failed: {e}")

                # Fallback to DALL-E 2
                try:
                    async with session.post(
                        f"{OPENROUTER_BASE_URL}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "openai/dall-e-2",
                            "messages": [{"role": "user", "content": f"Generate an image: {image_prompt}"}],
                            "max_tokens": 1000
                        }
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if "choices" in data and len(data["choices"]) > 0:
                                image_content = data["choices"][0]["message"]["content"]
                                if "http" in image_content:
                                    import re
                                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', image_content)
                                    if urls:
                                        logger.info("✅ Image generated successfully with DALL-E 2")
                                        return urls[0]
                except Exception as e:
                    logger.warning(f"DALL-E 2 failed: {e}")

                # Generate a professional placeholder image URL based on topic
                logger.info("🎨 Using professional placeholder image")
                return await self._generate_placeholder_image(topic)

        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return await self._generate_placeholder_image(topic)

    async def _generate_placeholder_image(self, topic: str) -> str:
        """Generate a professional placeholder image URL"""
        # Use a professional image service with topic-based images
        topic_clean = topic.replace(" ", "%20").replace(",", "").replace(".", "")

        # Try different professional image services
        image_services = [
            f"https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop&crop=center&auto=format&q=80&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # Professional business
            f"https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=600&fit=crop&crop=center&auto=format&q=80&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # Team meeting
            f"https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop&crop=center&auto=format&q=80&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # Office workspace
            f"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop&crop=center&auto=format&q=80&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # Professional person
        ]

        # Select image based on topic hash for consistency
        import hashlib
        topic_hash = int(hashlib.md5(topic.encode()).hexdigest(), 16)
        selected_image = image_services[topic_hash % len(image_services)]

        logger.info(f"📸 Using professional stock image for topic: {topic}")
        return selected_image

    async def _generate_with_openai(self, topic: str) -> Dict[str, Any]:
        """Generate content using OpenAI API with RAG enhancement"""
        try:
            import openai

            # Initialize OpenAI client
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

            # Get relevant context from RAG pipeline
            context_info = ""
            if RAG_AVAILABLE and 'rag' in self.models:
                try:
                    context_data = await rag_pipeline.get_relevant_context(topic, max_results=3)
                    if context_data:
                        context_info = "\n\nRelevant context:\n"
                        for item in context_data:
                            context_info += f"- {item.get('title', '')}: {item.get('content', '')}\n"
                except Exception as e:
                    logger.warning(f"Failed to get RAG context: {e}")

            # Generate text content with context
            text_prompt = f"""Create a professional LinkedIn post about: {topic}

            Requirements:
            - Professional tone
            - Engaging and informative
            - 150-300 words
            - Include a call to action
            - Use emojis sparingly but effectively
            - No hashtags (they will be generated separately)
            - Incorporate current trends and insights when relevant
            {context_info}
            """

            text_response = await client.chat.completions.create(
                model=getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "You are a professional LinkedIn content creator. Create engaging, professional posts that drive engagement and provide value."},
                    {"role": "user", "content": text_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            text_content = text_response.choices[0].message.content.strip()

            # Generate hashtags
            hashtag_prompt = f"""Generate 5-8 relevant professional hashtags for this LinkedIn post topic: {topic}

            Requirements:
            - Professional and relevant
            - Mix of popular and niche hashtags
            - Include # symbol
            - Return as a comma-separated list
            - Focus on business, professional development, and industry-specific tags
            """

            hashtag_response = await client.chat.completions.create(
                model=getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "You are a LinkedIn hashtag expert. Generate relevant, professional hashtags that will maximize post reach and engagement."},
                    {"role": "user", "content": hashtag_prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )

            hashtags_text = hashtag_response.choices[0].message.content.strip()
            hashtags = [tag.strip() for tag in hashtags_text.split(',') if tag.strip().startswith('#')]

            # Generate image using OpenRouter API (more reliable than OpenAI DALL-E)
            image_url = await self._generate_image_with_openrouter(topic, text_content)

            return {
                "text": text_content,
                "hashtags": hashtags,
                "image_url": image_url,
                "model_used": "openai-gpt"
            }

        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return await self._generate_mock_content(topic)
    
    async def _generate_mock_content(self, topic: str) -> Dict[str, Any]:
        """Generate mock content for development/fallback"""
        await asyncio.sleep(1)  # Simulate processing time

        # Use professional placeholder image even for mock content
        image_url = await self._generate_placeholder_image(topic)

        return {
            "text": f"Here are professional insights about {topic}. This content demonstrates the power of AI-driven content creation for LinkedIn professionals. \n\nKey benefits include:\n• Enhanced engagement\n• Time-saving automation\n• Consistent brand voice\n• Data-driven optimization\n\nWhat's your experience with AI content tools? Share your thoughts below! 👇",
            "hashtags": ["#AI", "#LinkedIn", "#ContentCreation", "#Productivity", "#DigitalMarketing", "#Innovation"],
            "image_url": image_url,
            "model_used": "mock"
        }
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        logger.info("🧹 Cleaning up AI models...")
        self.models.clear()
        self.loaded = False

# Global model manager instance
model_manager = ModelManager()
