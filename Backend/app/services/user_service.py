
from app.db.database import execute_query

def create_user(email: str, username: str, full_name: str, avatar_url: str = None, linkedin_profile_url: str = None, bio: str = None, industry: str = None, location: str = None):
    """Creates a new user in the database."""
    query = """
        INSERT INTO users (email, username, full_name, avatar_url, linkedin_profile_url, bio, industry, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, email, username, created_at;
    """
    params = (email, username, full_name, avatar_url, linkedin_profile_url, bio, industry, location)
    return execute_query(query, params, fetch="one")

def get_user_by_email(email: str):
    """Retrieves a user by their email address."""
    query = "SELECT * FROM users WHERE email = %s;"
    return execute_query(query, (email,), fetch="one")

def get_user_by_username(username: str):
    """Retrieves a user by their username."""
    query = "SELECT * FROM users WHERE username = %s;"
    return execute_query(query, (username,), fetch="one")

def get_user_profile(email: str):
    """Retrieves a user's profile data."""
    user = get_user_by_email(email)
    if not user:
        return None

    # For now, we'll just return the user data.
    # In the future, we can add more complex logic to analyze the profile.
    return user
