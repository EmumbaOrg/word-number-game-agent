session = {}
users = {}

def get_user_session(user_id: str) -> dict:
    """
    Get the current user session.
    """
    user = session.get(user_id, None)
    if user is None:
        return None
    
    return session[f"{user_id}"]

def create_user_session(user_id: str) -> None:
    """
    Create a new user session.
    """
    session[user_id] = user_id

def get_user(user_id: str) -> dict:
    users = users.get(user_id, None)
    if users is None:
        return None
    return users[f"{user_id}"]

def create_user(user_id: str, name: str) -> None:
    """
    Create a new user.
    """
    users[user_id] = {
        "user_id": user_id,
        "name": name,
    }
    return users[user_id]