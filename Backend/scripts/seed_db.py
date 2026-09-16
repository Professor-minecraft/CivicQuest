import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import engine, Base
from app.main import seed_default_accounts

def main():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Seeding default accounts (admin@gg, auditor@gg)...")
    seed_default_accounts()
    print("Database initialization and seed complete!")

if __name__ == "__main__":
    main()
