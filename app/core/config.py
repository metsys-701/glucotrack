from datetime import timedelta

# JWT Configuration
SECRET_KEY = "your-secret-key-here-change-in-production-min-32-characters"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour