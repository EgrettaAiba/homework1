import json
import uuid
from datetime import datetime
from typing import Any, Dict, List


# JSON database functions
async def read_json(file_path: str) -> List[Dict[str, Any]]:
    """Read data from JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []


async def write_json(file_path: str, data: List[Dict[str, Any]]) -> bool:
    """Write data to JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False


async def get_all_users() -> List[Dict[str, Any]]:
    """Get all users from database."""
    return await read_json("data/users.json")


async def save_user(user: Dict[str, Any]) -> bool:
    """Save user to database."""
    users = await get_all_users()
    users.append(user)
    return await write_json("data/users.json", users)


async def get_all_posts() -> List[Dict[str, Any]]:
    """Get all posts from database."""
    return await read_json("data/posts.json")


async def save_post(post: Dict[str, Any]) -> bool:
    """Save post to database."""
    posts = await get_all_posts()
    posts.append(post)
    return await write_json("data/posts.json", posts)


async def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """Get user by ID."""
    users = await get_all_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return {}


async def get_posts_by_user(user_id: str) -> List[Dict[str, Any]]:
    """Get posts by user ID."""
    posts = await get_all_posts()
    return [post for post in posts if post["author_id"] == user_id]


def generate_id() -> str:
    """Generate unique ID."""
    return str(uuid.uuid4())


def get_current_time() -> str:
    """Get current timestamp."""
    return datetime.now().isoformat()
