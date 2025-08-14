
from app.db.database import execute_query
from datetime import datetime

def schedule_post(user_id: str, content: str, scheduled_time: datetime, hashtags: list = None, image_url: str = None):
    """Schedules a new post for a user."""
    query = """
        INSERT INTO scheduled_posts (user_id, content, scheduled_time, hashtags, image_url)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, user_id, content, scheduled_time, status;
    """
    params = (user_id, content, scheduled_time, hashtags, image_url)
    return execute_query(query, params, fetch="one")

def get_scheduled_posts(user_id: str):
    """Retrieves all scheduled posts for a user."""
    query = "SELECT * FROM scheduled_posts WHERE user_id = %s ORDER BY scheduled_time ASC;"
    return execute_query(query, (user_id,), fetch="all")

def generate_intelligent_post(topic: str, user_profile: dict):
    """Generates an intelligent post based on the user's profile."""
    # This is a simplified example. In a real application, we would use a more
    # sophisticated prompt engineering approach.
    prompt = f"""Create a professional LinkedIn post about: {topic}

    Your post should be tailored to a {user_profile.get('role', 'professional')} in the {user_profile.get('industry', 'business')} industry.
    The tone should be {user_profile.get('brand_voice', 'professional')}.
    Focus on topics like {', '.join(user_profile.get('interests', []))}.

    Requirements:
    - Professional tone suitable for LinkedIn
    - 150-250 words
    - Include key insights and actionable advice
    - End with an engaging question
    - No hashtags (will be generated separately)

    Topic: {topic}"""

    # For now, we will just return the prompt for demonstration purposes.
    # In a real implementation, we would send this prompt to an LLM.
    return {
        "text": prompt,
        "hashtags": ["#intelligentcontent", f"#{user_profile.get('industry', 'business')}"],
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop",
        "model_used": "intelligent-mock"
    }
