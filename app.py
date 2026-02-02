from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_
import os

from config import Config
from models import db, User, Task, Attendance
from forms import LoginForm, StudentRegistrationForm, TaskForm, TaskUpdateForm, AttendanceForm, ChangePasswordForm, EditProfileForm, ForgotPasswordForm

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
    
    return app

app = create_app()

# Add date to template context
@app.context_processor
def inject_date():
    return {'date': date}

# Helper function to check admin role
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Authentication Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=True)
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        # Find user by username and email
        user = User.query.filter_by(
            username=form.username.data,
            email=form.email.data
        ).first()
        
        if user:
            # Update password
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been reset successfully! You can now login with your new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username and email combination not found.', 'error')
    
    return render_template('auth/forgot_password.html', form=form)

# Admin Routes
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Get statistics
    total_students = User.query.filter_by(role='student', is_active=True).count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    
    # Calculate task completion percentage
    task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Get attendance statistics for today
    today = date.today()
    present_today = Attendance.query.filter_by(date=today, status='present').count()
    total_attendance_today = Attendance.query.filter_by(date=today).count()
    attendance_rate = (present_today / total_attendance_today * 100) if total_attendance_today > 0 else 0
    
    # Recent activities
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    recent_attendance = Attendance.query.filter_by(date=today).order_by(Attendance.marked_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         task_completion_rate=round(task_completion_rate, 1),
                         attendance_rate=round(attendance_rate, 1),
                         recent_tasks=recent_tasks,
                         recent_attendance=recent_attendance)

@app.route('/admin/students')
@login_required
@admin_required
def admin_students():
    students = User.query.filter_by(role='student').order_by(User.full_name).all()
    return render_template('admin/students.html', students=students)

@app.route('/admin/students/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        student = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role='student'
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash(f'Student account created successfully for {student.full_name}!', 'success')
        return redirect(url_for('admin_students'))
    
    return render_template('admin/create_student.html', form=form)

@app.route('/admin/students/<int:student_id>/toggle')
@login_required
@admin_required
def toggle_student_status(student_id):
    student = User.query.get_or_404(student_id)
    if student.role != 'student':
        flash('Invalid operation.', 'error')
        return redirect(url_for('admin_students'))
    
    student.is_active = not student.is_active
    db.session.commit()
    status = 'activated' if student.is_active else 'deactivated'
    flash(f'Student {student.full_name} has been {status}.', 'success')
    return redirect(url_for('admin_students'))

@app.route('/admin/tasks')
@login_required
@admin_required
def admin_tasks():
    tasks = Task.query.order_by(Task.due_date.desc()).all()
    return render_template('admin/tasks.html', tasks=tasks)

@app.route('/admin/tasks/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_task():
    form = TaskForm()
    # Populate student choices
    students = User.query.filter_by(role='student', is_active=True).all()
    form.student_id.choices = [(s.id, s.full_name) for s in students]
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            student_id=form.student_id.data,
            created_by=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('admin_tasks'))
    
    return render_template('admin/create_task.html', form=form)

@app.route('/admin/attendance')
@login_required
@admin_required
def admin_attendance():
    # Get attendance for today by default
    selected_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    attendance_records = Attendance.query.filter_by(date=selected_date).all()
    students = User.query.filter_by(role='student', is_active=True).all()
    
    return render_template('admin/attendance.html', 
                         attendance_records=attendance_records,
                         students=students,
                         selected_date=selected_date)

@app.route('/admin/attendance/mark', methods=['GET', 'POST'])
@login_required
@admin_required
def mark_attendance():
    form = AttendanceForm()
    students = User.query.filter_by(role='student', is_active=True).all()
    form.student_id.choices = [(s.id, s.full_name) for s in students]
    
    if form.validate_on_submit():
        # Check if attendance already exists for this student and date
        existing = Attendance.query.filter_by(
            student_id=form.student_id.data,
            date=form.date.data
        ).first()
        
        if existing:
            flash('Attendance already marked for this student on this date.', 'warning')
        else:
            attendance = Attendance(
                date=form.date.data,
                student_id=form.student_id.data,
                status=form.status.data,
                remarks=form.remarks.data,
                marked_by=current_user.id
            )
            db.session.add(attendance)
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
        
        return redirect(url_for('admin_attendance'))
    
    return render_template('admin/mark_attendance.html', form=form)

@app.route('/admin/edit-profile', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('admin/edit_profile.html', form=form)

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Check if current password is correct
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('admin/change_password.html', form=form)
        
        # Update password
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been changed successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/change_password.html', form=form)

# Student Routes
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    # Get student's tasks
    pending_tasks = Task.query.filter_by(student_id=current_user.id, status='pending').count()
    in_progress_tasks = Task.query.filter_by(student_id=current_user.id, status='in_progress').count()
    completed_tasks = Task.query.filter_by(student_id=current_user.id, status='completed').count()
    
    # Get recent tasks
    recent_tasks = Task.query.filter_by(student_id=current_user.id).order_by(Task.created_at.desc()).limit(5).all()
    
    # Get attendance summary for current month
    current_month = date.today().replace(day=1)
    attendance_records = Attendance.query.filter(
        and_(Attendance.student_id == current_user.id,
             Attendance.date >= current_month)
    ).all()
    
    present_days = len([a for a in attendance_records if a.status == 'present'])
    total_days = len(attendance_records)
    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
    
    return render_template('student/dashboard.html',
                         pending_tasks=pending_tasks,
                         in_progress_tasks=in_progress_tasks,
                         completed_tasks=completed_tasks,
                         recent_tasks=recent_tasks,
                         attendance_rate=round(attendance_rate, 1),
                         present_days=present_days,
                         total_days=total_days)

@app.route('/student/tasks')
@login_required
def student_tasks():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    status_filter = request.args.get('status', 'all')
    
    query = Task.query.filter_by(student_id=current_user.id)
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    tasks = query.order_by(Task.due_date.asc()).all()
    
    return render_template('student/tasks.html', tasks=tasks, status_filter=status_filter)

@app.route('/student/tasks/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Ensure student can only update their own tasks
    if task.student_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('student_tasks'))
    
    form = TaskUpdateForm()
    if form.validate_on_submit():
        task.status = form.status.data
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task status updated successfully!', 'success')
        return redirect(url_for('student_tasks'))
    
    form.status.data = task.status
    return render_template('student/update_task.html', form=form, task=task)

@app.route('/student/attendance')
@login_required
def student_attendance():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    # Get attendance records for current month by default
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    year, month_num = map(int, month.split('-'))
    
    # Get first and last day of the month
    first_day = date(year, month_num, 1)
    if month_num == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month_num + 1, 1) - timedelta(days=1)
    
    attendance_records = Attendance.query.filter(
        and_(Attendance.student_id == current_user.id,
             Attendance.date >= first_day,
             Attendance.date <= last_day)
    ).order_by(Attendance.date.desc()).all()
    
    return render_template('student/attendance.html', 
                         attendance_records=attendance_records,
                         selected_month=month)

@app.route('/student/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Check if current password is correct
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('student/change_password.html', form=form)
        
        # Update password
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been changed successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/change_password.html', form=form)

@app.route('/student/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('student/edit_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)