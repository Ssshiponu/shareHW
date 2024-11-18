from app import redis_client
from functools import wraps
import json
from datetime import datetime

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def cache_key(*args, **kwargs):
    """Generate a cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def cache(timeout=300):
    """
    Cache decorator that uses Redis
    timeout: cache duration in seconds (default 5 minutes)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            key = f"{f.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get cached value
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
            
            # If not cached, execute function and cache result
            result = f(*args, **kwargs)
            redis_client.setex(
                key,
                timeout,
                json.dumps(result, default=serialize_datetime)
            )
            return result
        return decorated_function
    return decorator

def invalidate_cache(pattern):
    """Invalidate all cache keys matching the pattern"""
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)

# Cache keys for different content types
CACHE_KEYS = {
    'recent_homework': 'homework:recent:{}:{}',  # format with class_name, section
    'homework_by_date': 'homework:date:{}:{}:{}',  # format with class_name, section, date
    'notes_by_subject': 'notes:subject:{}:{}:{}',  # format with class_name, section, subject
    'user_profile': 'user:{}',  # format with user_id
    'pending_approvals': 'pending:{}:{}',  # format with class_name, section
}
