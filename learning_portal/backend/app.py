from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from werkzeug.utils import secure_filename

# Obtener la ruta absoluta del directorio del proyecto
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(project_dir, 'database')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Crear la aplicación Flask
app = Flask(__name__, template_folder=os.path.join(project_dir, 'frontend', 'templates'), static_folder=os.path.join(project_dir, 'frontend', 'static'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey'

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_dir, 'database', 'learning_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Modelos de la Base de Datos ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='student')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor = db.Column(db.String(120), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    resources_link = db.Column(db.String(200), nullable=True)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('modules', lazy=True))

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'video', 'document'
    content_url = db.Column(db.String(200), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    module = db.relationship('Module', backref=db.backref('lessons', lazy=True))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson = db.relationship('Lesson', backref=db.backref('quizzes', lazy=True))
    time_limit = db.Column(db.Integer, nullable=True) # in minutes

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))
    progress = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='in_progress') # 'in_progress', 'completed'
    due_date = db.Column(db.DateTime, nullable=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def import_courses_from_excel(filepath):
    try:
        df = pd.read_excel(filepath)
        for index, row in df.iterrows():
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
        flash('Courses imported successfully.')
    except Exception as e:
        flash(f"Error importing courses: {e}")
        db.session.rollback()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

@app.route('/upload_courses', methods=['GET', 'POST'])
def upload_courses():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            import_courses_from_excel(filepath)
            return redirect(url_for('index'))
    return render_template('upload.html')

# --- API Endpoints ---

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'instructor': course.instructor,
        'duration': course.duration
    } for course in courses])

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'instructor': course.instructor,
        'duration': course.duration,
        'modules': [{'id': module.id, 'title': module.title} for module in course.modules]
    })

@app.route('/api/reports/user/<int:user_id>', methods=['GET'])
def get_user_report(user_id):
    from .reporter import generate_user_performance_report
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'user_{user_id}_report.xlsx')
    generate_user_performance_report(user_id, output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/api/reports/completion', methods=['GET'])
def get_completion_report():
    from .reporter import generate_completion_statistics_report
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'completion_report.xlsx')
    generate_completion_statistics_report(output_path)
    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
