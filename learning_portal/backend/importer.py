import pandas as pd
from .app import db, Course

def import_courses_from_excel(filepath):
    try:
        df = pd.read_excel(filepath)
        for index, row in df.iterrows():
            # Validar datos
            if Course.query.filter_by(name=row['name']).first():
                print(f"Course '{row['name']}' already exists. Skipping.")
                continue

            new_course = Course(
                name=row['name'],
                description=row.get('description', ''),
                instructor=row.get('instructor', ''),
                duration=row.get('duration', None),
                resources_link=row.get('resources_link', '')
            )
            db.session.add(new_course)
        db.session.commit()
        print("Courses imported successfully.")
    except Exception as e:
        print(f"Error importing courses: {e}")
        db.session.rollback()
