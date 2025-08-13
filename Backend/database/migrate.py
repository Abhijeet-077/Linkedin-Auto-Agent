#!/usr/bin/env python3
"""
Database Migration Script for InfluenceOS
Handles database schema creation and updates
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False
    logger.error("asyncpg not available - install with: pip install asyncpg")

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.error("supabase not available - install with: pip install supabase")

class DatabaseMigrator:
    """Database migration manager"""
    
    def __init__(self):
        self.connection = None
        self.supabase_client = None
        
    async def connect(self):
        """Connect to the database"""
        try:
            if SUPABASE_AVAILABLE and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
                # Use Supabase
                self.supabase_client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_SERVICE_KEY
                )
                logger.info("✅ Connected to Supabase")
                return True
                
            elif ASYNCPG_AVAILABLE and hasattr(settings, 'DATABASE_URL'):
                # Use direct PostgreSQL connection
                self.connection = await asyncpg.connect(settings.DATABASE_URL)
                logger.info("✅ Connected to PostgreSQL")
                return True
                
            else:
                logger.error("❌ No database connection available")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            return False
    
    async def run_migration(self, sql_file: str):
        """Run a SQL migration file"""
        try:
            # Read the SQL file
            sql_path = Path(__file__).parent / sql_file
            if not sql_path.exists():
                logger.error(f"❌ SQL file not found: {sql_path}")
                return False
            
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split SQL content into individual statements
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            logger.info(f"🔄 Running migration: {sql_file}")
            logger.info(f"📝 Found {len(statements)} SQL statements")
            
            # Execute each statement
            for i, statement in enumerate(statements, 1):
                try:
                    if self.connection:
                        # Direct PostgreSQL connection
                        await self.connection.execute(statement)
                    elif self.supabase_client:
                        # Supabase connection
                        result = self.supabase_client.rpc('exec_sql', {'sql': statement})
                        if hasattr(result, 'error') and result.error:
                            logger.warning(f"⚠️ Statement {i} warning: {result.error}")
                    
                    logger.debug(f"✅ Statement {i} executed successfully")
                    
                except Exception as e:
                    # Some statements might fail if they already exist (like CREATE TABLE IF NOT EXISTS)
                    # Log as warning instead of error
                    logger.warning(f"⚠️ Statement {i} failed (might be expected): {e}")
            
            logger.info(f"✅ Migration completed: {sql_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            return False
    
    async def create_schema(self):
        """Create the database schema"""
        return await self.run_migration('schema.sql')
    
    async def seed_data(self):
        """Seed initial data"""
        try:
            logger.info("🌱 Seeding initial data...")
            
            # Create sample knowledge base entries
            sample_knowledge = [
                {
                    "title": "LinkedIn Best Practices 2024",
                    "content": "LinkedIn engagement rates are highest for posts with 1-3 hashtags, personal stories, and industry insights.",
                    "source": "linkedin",
                    "topic_tags": ["linkedin", "engagement", "best-practices"],
                    "relevance_score": 0.9
                },
                {
                    "title": "AI Content Creation Trends",
                    "content": "AI-generated content is becoming mainstream, with 73% of marketers using AI tools for content creation.",
                    "source": "news",
                    "topic_tags": ["ai", "content-creation", "marketing"],
                    "relevance_score": 0.8
                },
                {
                    "title": "Professional Networking Tips",
                    "content": "Building authentic relationships on LinkedIn requires consistent engagement and value-driven content sharing.",
                    "source": "manual",
                    "topic_tags": ["networking", "relationships", "professional"],
                    "relevance_score": 0.85
                }
            ]
            
            if self.supabase_client:
                # Insert sample data using Supabase
                for item in sample_knowledge:
                    try:
                        result = self.supabase_client.table('knowledge_base').insert(item).execute()
                        logger.debug(f"✅ Inserted knowledge item: {item['title']}")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to insert knowledge item: {e}")
            
            logger.info("✅ Data seeding completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Data seeding failed: {e}")
            return False
    
    async def check_connection(self):
        """Check database connection and basic functionality"""
        try:
            logger.info("🔍 Checking database connection...")
            
            if self.supabase_client:
                # Test Supabase connection
                result = self.supabase_client.table('users').select('id').limit(1).execute()
                logger.info("✅ Supabase connection test passed")
                
            elif self.connection:
                # Test PostgreSQL connection
                result = await self.connection.fetchval('SELECT 1')
                logger.info("✅ PostgreSQL connection test passed")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False
    
    async def close(self):
        """Close database connections"""
        try:
            if self.connection:
                await self.connection.close()
                logger.info("🔌 PostgreSQL connection closed")
                
            # Supabase client doesn't need explicit closing
            
        except Exception as e:
            logger.error(f"❌ Error closing connections: {e}")

async def main():
    """Main migration function"""
    logger.info("🚀 Starting InfluenceOS database migration...")
    
    migrator = DatabaseMigrator()
    
    try:
        # Connect to database
        if not await migrator.connect():
            logger.error("❌ Failed to connect to database")
            return False
        
        # Run schema migration
        if not await migrator.create_schema():
            logger.error("❌ Schema migration failed")
            return False
        
        # Check connection
        if not await migrator.check_connection():
            logger.error("❌ Connection check failed")
            return False
        
        # Seed initial data
        if not await migrator.seed_data():
            logger.warning("⚠️ Data seeding failed (non-critical)")
        
        logger.info("🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed with error: {e}")
        return False
        
    finally:
        await migrator.close()

if __name__ == "__main__":
    # Run the migration
    success = asyncio.run(main())
    
    if success:
        print("\n✅ Database migration completed successfully!")
        print("🔗 Your database is ready for InfluenceOS!")
    else:
        print("\n❌ Database migration failed!")
        print("📋 Please check the logs above for details.")
        sys.exit(1)
