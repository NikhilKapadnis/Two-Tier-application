# ============================================================
#  config.py — All config read from environment variables
#  Never hardcode credentials — ECS injects these at runtime
#  via task definition environment vars or Secrets Manager
# ============================================================

import os

class Config:
    # ----------------------------------------------------------
    # PostgreSQL connection string built from individual env vars
    # Format: postgresql://user:password@host:port/dbname
    # ----------------------------------------------------------
    DB_USER     = os.environ.get("DB_USER",     "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "mypassword1282000")
    DB_HOST     = os.environ.get("DB_HOST",     "306616136846.dkr.ecr.ap-south-1.amazonaws.com/two-tier-application")
    DB_PORT     = os.environ.get("DB_PORT",     "5432")
    DB_NAME     = os.environ.get("DB_NAME",     "myappdb")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------------------------------------------------
    # Flask secret key — used for sessions/cookies
    # ----------------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
