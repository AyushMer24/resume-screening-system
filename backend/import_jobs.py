import csv
from backend.database import SessionLocal
from backend.models import Job

def import_jobs(csv_file):
    db = SessionLocal()

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        jobs = []

        for row in reader:
            jobs.append(
                Job(
                    title=row["title"],
                    description=row["description"]
                )
            )

        db.bulk_save_objects(jobs)
        db.commit()
        db.close()

    print(f"✅ Imported {len(jobs)} jobs")

if __name__ == "__main__":
    import_jobs("jobs.csv")