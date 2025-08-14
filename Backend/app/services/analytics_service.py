
from app.db.database import execute_query

def get_total_posts(user_id: str):
    """Gets the total number of posts for a user."""
    query = "SELECT COUNT(*) as total_posts FROM scheduled_posts WHERE user_id = %s AND status = 'published';"
    result = execute_query(query, (user_id,), fetch="one")
    return result['total_posts'] if result else 0

def get_total_likes(user_id: str):
    """Gets the total number of likes for a user's posts."""
    query = """
        SELECT SUM((engagement_metrics->>'likes')::int) as total_likes
        FROM scheduled_posts
        WHERE user_id = %s AND status = 'published' AND engagement_metrics->>'likes' IS NOT NULL;
    """
    result = execute_query(query, (user_id,), fetch="one")
    return result['total_likes'] if result and result['total_likes'] is not None else 0

def get_basic_analytics(user_id: str):
    """Gets basic analytics for a user."""
    total_posts = get_total_posts(user_id)
    total_likes = get_total_likes(user_id)
    # In a real application, we would calculate engagement rate and other metrics.
    # For now, we'll return some static data alongside the real data.
    return {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "engagement_rate": 4.2, # static for now
        "total_comments": 89, # static for now
        "total_shares": 34, # static for now
        "growth_rate": 15.3 # static for now
    }
