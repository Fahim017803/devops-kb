import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-dev-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 8   # 8 hours
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER', 'devops_user')}"
        f":{os.environ.get('DB_PASSWORD', 'devops_pass')}"
        f"@{os.environ.get('DB_HOST', 'db')}"
        f":{os.environ.get('DB_PORT', '3306')}"
        f"/{os.environ.get('DB_NAME', 'devops_kb')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
