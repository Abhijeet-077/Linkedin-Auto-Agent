"""
RAG (Retrieval-Augmented Generation) Pipeline
Provides up-to-date information for content generation
"""
import asyncio
import json
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("Sentence transformers not available - install with: pip install sentence-transformers")

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not available - install with: pip install chromadb")

class RAGPipeline:
    """Retrieval-Augmented Generation Pipeline"""
    
    def __init__(self):
        self.embedding_model = None
        self.vector_db = None
        self.initialized = False
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        
    async def initialize(self):
        """Initialize RAG pipeline components"""
        try:
            logger.info("🔍 Initializing RAG pipeline...")
            
            # Initialize embedding model
            if EMBEDDINGS_AVAILABLE:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Embedding model loaded")
            
            # Initialize vector database
            if CHROMADB_AVAILABLE:
                self.vector_db = chromadb.Client()
                self.collection = self.vector_db.create_collection(
                    name="linkedin_content_knowledge",
                    get_or_create=True
                )
                logger.info("✅ Vector database initialized")
            
            self.initialized = True
            logger.info("✅ RAG pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize RAG pipeline: {e}")
            self.initialized = True  # Allow fallback mode
    
    async def get_relevant_context(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a topic"""
        if not self.initialized:
            await self.initialize()
        
        try:
            # Check cache first
            cache_key = f"context_{topic}_{max_results}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                    return cached_data
            
            # Gather context from multiple sources
            context = []
            
            # 1. Get trending topics
            trending_data = await self._get_trending_topics(topic)
            context.extend(trending_data)
            
            # 2. Get industry news
            news_data = await self._get_industry_news(topic)
            context.extend(news_data)
            
            # 3. Get LinkedIn insights
            linkedin_data = await self._get_linkedin_insights(topic)
            context.extend(linkedin_data)
            
            # 4. Query vector database if available
            if self.vector_db and EMBEDDINGS_AVAILABLE:
                vector_data = await self._query_vector_db(topic, max_results)
                context.extend(vector_data)
            
            # Rank and filter results
            ranked_context = await self._rank_context(context, topic, max_results)
            
            # Cache results
            self.cache[cache_key] = (ranked_context, datetime.now())
            
            return ranked_context
            
        except Exception as e:
            logger.error(f"Failed to get relevant context: {e}")
            return []
    
    async def _get_trending_topics(self, topic: str) -> List[Dict[str, Any]]:
        """Get trending topics related to the subject"""
        try:
            # Mock trending topics for now
            # In production, this would connect to Twitter API, Google Trends, etc.
            trending_topics = [
                {
                    "source": "trending",
                    "title": f"Latest trends in {topic}",
                    "content": f"Current market trends show increased interest in {topic} with 25% growth in engagement",
                    "relevance_score": 0.8,
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "source": "trending",
                    "title": f"{topic} industry insights",
                    "content": f"Industry leaders are focusing on {topic} as a key driver for digital transformation",
                    "relevance_score": 0.7,
                    "timestamp": datetime.now().isoformat()
                }
            ]
            
            return trending_topics
            
        except Exception as e:
            logger.error(f"Failed to get trending topics: {e}")
            return []
    
    async def _get_industry_news(self, topic: str) -> List[Dict[str, Any]]:
        """Get recent industry news"""
        try:
            # Mock news data for now
            # In production, this would connect to news APIs like NewsAPI, Google News, etc.
            news_items = [
                {
                    "source": "news",
                    "title": f"Breaking: Major developments in {topic}",
                    "content": f"Recent studies show that {topic} is becoming increasingly important for business success",
                    "relevance_score": 0.9,
                    "timestamp": datetime.now().isoformat(),
                    "url": "https://example.com/news"
                },
                {
                    "source": "news",
                    "title": f"Expert analysis on {topic} trends",
                    "content": f"Industry experts predict significant growth in {topic} adoption over the next year",
                    "relevance_score": 0.8,
                    "timestamp": datetime.now().isoformat(),
                    "url": "https://example.com/analysis"
                }
            ]
            
            return news_items
            
        except Exception as e:
            logger.error(f"Failed to get industry news: {e}")
            return []
    
    async def _get_linkedin_insights(self, topic: str) -> List[Dict[str, Any]]:
        """Get LinkedIn-specific insights and best practices"""
        try:
            # Mock LinkedIn insights
            # In production, this would analyze successful LinkedIn posts, engagement patterns, etc.
            insights = [
                {
                    "source": "linkedin",
                    "title": f"LinkedIn best practices for {topic} content",
                    "content": f"Posts about {topic} perform 40% better when they include personal experiences and actionable insights",
                    "relevance_score": 0.9,
                    "timestamp": datetime.now().isoformat(),
                    "engagement_data": {
                        "avg_likes": 150,
                        "avg_comments": 25,
                        "avg_shares": 10
                    }
                },
                {
                    "source": "linkedin",
                    "title": f"Optimal posting times for {topic}",
                    "content": f"Content about {topic} gets maximum engagement when posted on Tuesday-Thursday, 9-11 AM",
                    "relevance_score": 0.7,
                    "timestamp": datetime.now().isoformat(),
                    "engagement_data": {
                        "peak_hours": ["9:00", "10:00", "11:00"],
                        "peak_days": ["Tuesday", "Wednesday", "Thursday"]
                    }
                }
            ]
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get LinkedIn insights: {e}")
            return []
    
    async def _query_vector_db(self, topic: str, max_results: int) -> List[Dict[str, Any]]:
        """Query vector database for similar content"""
        try:
            if not self.embedding_model or not self.vector_db:
                return []
            
            # Generate embedding for the topic
            topic_embedding = self.embedding_model.encode([topic])
            
            # Query the vector database
            results = self.collection.query(
                query_embeddings=topic_embedding.tolist(),
                n_results=max_results
            )
            
            # Format results
            vector_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results.get('documents', []),
                results.get('metadatas', []),
                results.get('distances', [])
            )):
                vector_results.append({
                    "source": "vector_db",
                    "title": metadata.get('title', f'Related content {i+1}'),
                    "content": doc,
                    "relevance_score": 1.0 - distance,  # Convert distance to similarity
                    "timestamp": metadata.get('timestamp', datetime.now().isoformat())
                })
            
            return vector_results
            
        except Exception as e:
            logger.error(f"Failed to query vector database: {e}")
            return []
    
    async def _rank_context(self, context: List[Dict[str, Any]], topic: str, max_results: int) -> List[Dict[str, Any]]:
        """Rank and filter context by relevance"""
        try:
            # Sort by relevance score
            ranked = sorted(context, key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Return top results
            return ranked[:max_results]
            
        except Exception as e:
            logger.error(f"Failed to rank context: {e}")
            return context[:max_results]
    
    async def add_to_knowledge_base(self, content: str, metadata: Dict[str, Any]):
        """Add content to the knowledge base"""
        try:
            if not self.vector_db or not self.embedding_model:
                return
            
            # Generate embedding
            embedding = self.embedding_model.encode([content])
            
            # Add to vector database
            self.collection.add(
                documents=[content],
                embeddings=embedding.tolist(),
                metadatas=[metadata],
                ids=[f"doc_{datetime.now().timestamp()}"]
            )
            
            logger.info("✅ Content added to knowledge base")
            
        except Exception as e:
            logger.error(f"Failed to add to knowledge base: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up RAG pipeline...")
        self.cache.clear()
        self.initialized = False

# Global RAG pipeline instance
rag_pipeline = RAGPipeline()
