import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
