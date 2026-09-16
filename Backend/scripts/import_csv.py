import sys
import argparse
from pathlib import Path

# Add Backend root to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal, engine, Base
from app.services.csv_import import import_csv_to_db
from app.config import settings

def main():
    parser = argparse.ArgumentParser(description="Import works_completed.csv dataset into CivicQuest database.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of records to import (for quick testing).")
    parser.add_argument("--batch-size", type=int, default=500, help="Batch size for database insertions.")
    parser.add_argument("--file", type=str, default=None, help="Custom path to CSV file.")
    args = parser.parse_args()

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    csv_path = Path(args.file) if args.file else settings.resolved_csv_path
    print(f"Starting import from: {csv_path}")
    print(f"Record limit: {args.limit or 'ALL records'}")

    db = SessionLocal()
    try:
        results = import_csv_to_db(db, csv_path=csv_path, limit=args.limit, batch_size=args.batch_size)
        print("\n--- Import Summary ---")
        print(f"Total rows processed: {results['total_processed']}")
        print(f"New records inserted: {results['inserted']}")
        print(f"Existing updated:     {results['updated']}")
        print("CSV Import successfully completed!")
    except Exception as e:
        print(f"Error during CSV import: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
