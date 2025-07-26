import pandas as pd
from .app import db, Enrollment, User, Course

def generate_user_performance_report(user_id, output_path):
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    if not enrollments:
        print("No enrollments found for this user.")
        return

    data = {
        'Course Name': [e.course.name for e in enrollments],
        'Status': [e.status for e in enrollments],
        'Progress': [e.progress for e in enrollments],
        'Due Date': [e.due_date for e in enrollments]
    }
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    print(f"Report generated for user {user_id} at {output_path}")

def generate_completion_statistics_report(output_path):
    courses = Course.query.all()
    data = {
        'Course Name': [c.name for c in courses],
        'Completions': [len([e for e in c.enrollments if e.status == 'completed']) for c in courses],
        'In Progress': [len([e for e in c.enrollments if e.status == 'in_progress']) for c in courses]
    }
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    print(f"Completion statistics report generated at {output_path}")
