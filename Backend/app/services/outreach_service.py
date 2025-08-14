
from app.db.database import execute_query

def get_outreach_campaigns(user_id: str):
    """Retrieves all outreach campaigns for a user."""
    query = "SELECT * FROM outreach_campaigns WHERE user_id = %s ORDER BY created_at DESC;"
    return execute_query(query, (user_id,), fetch="all")

def create_outreach_campaign(user_id: str, name: str, description: str, target_audience: str, message_template: str):
    """Creates a new outreach campaign for a user."""
    query = """
        INSERT INTO outreach_campaigns (user_id, name, description, target_audience, message_template)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, user_id, name, status, created_at;
    """
    params = (user_id, name, description, target_audience, message_template)
    return execute_query(query, params, fetch="one")
