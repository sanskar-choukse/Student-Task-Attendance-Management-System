# Student Task & Attendance Management System

A comprehensive Flask web application for managing student tasks and attendance with role-based authentication.

## Features

### Admin Features
- **Dashboard**: Overview of system statistics including total students, task completion rates, and attendance percentages
- **Student Management**: Create, view, and manage student accounts
- **Task Management**: Create and assign tasks to students with priorities and due dates
- **Attendance Management**: Mark daily attendance for students with status tracking

### Student Features
- **Dashboard**: Personal overview with task statistics and attendance summary
- **Task Management**: View assigned tasks, update task status (pending → in progress → completed)
- **Attendance Tracking**: View personal attendance records with monthly filtering

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Database**: SQLite (development)
- **Authentication**: Flask-Login with role-based access control
- **Forms**: Flask-WTF with validation

## Project Structure

```
student-management-system/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── forms.py              # WTForms for validation
├── config.py             # Configuration settings
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── static/
│   └── css/
│       └── style.css     # Custom CSS styling
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── auth/
│   │   └── login.html    # Login page
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── students.html
│   │   ├── create_student.html
│   │   ├── tasks.html
│   │   ├── create_task.html
│   │   ├── attendance.html
│   │   └── mark_attendance.html
│   └── student/
│       ├── dashboard.html
│       ├── tasks.html
│       ├── update_task.html
│       └── attendance.html
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download
Download all the project files to your local directory.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python main.py
```

The application will start on `http://localhost:5000`

## Default Login Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### Student Accounts
Student accounts need to be created by the admin through the admin panel.

## Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Create Students**: Navigate to "Students" → "Add New Student"
3. **Create Tasks**: Go to "Tasks" → "Create New Task" and assign to students
4. **Mark Attendance**: Use "Attendance" → "Mark Attendance" for daily tracking
5. **Monitor Progress**: Use the dashboard to view system statistics

### For Students

1. **Login** with credentials provided by admin
2. **View Tasks**: Check assigned tasks and their due dates
3. **Update Progress**: Change task status as you work on them
4. **Check Attendance**: View your attendance records and statistics

## Database Models

### User Model
- Handles both admin and student accounts
- Role-based authentication (admin/student)
- Password hashing for security

### Task Model
- Task assignment and tracking
- Priority levels (low, medium, high)
- Status tracking (pending, in progress, completed)

### Attendance Model
- Daily attendance tracking
- Status options (present, absent, late)
- Remarks for additional notes

## Key Features

### Security
- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Role-based access control
- Session management with Flask-Login

### User Experience
- Responsive design for mobile and desktop
- Clean, modern interface
- Flash messages for user feedback
- Form validation with error handling

### Data Management
- SQLAlchemy ORM for database operations
- Proper foreign key relationships
- Data validation at model level

## Customization

### Styling
Modify `static/css/style.css` to customize the appearance.

### Database
Change the database URI in `config.py` for production use:
```python
SQLALCHEMY_DATABASE_URI = 'your-production-database-url'
```

### Email Configuration
Add email settings in `config.py` for password reset functionality (future enhancement).

## Production Deployment

For production deployment:

1. Set environment variables:
   ```bash
   export SECRET_KEY="your-secret-key"
   export DATABASE_URL="your-database-url"
   ```

2. Use a production WSGI server like Gunicorn. Add `gunicorn` to `requirements.txt` and use a start command that binds to the port provided by the hosting environment (Render sets `$PORT` automatically):
   ```bash
   pip install gunicorn
   gunicorn main:app --bind 0.0.0.0:$PORT
   ```

   - On Render, make sure your service is created as a **Web Service** (not a Static Site) and set the **Start Command** to:
   ```bash
   gunicorn main:app --bind 0.0.0.0:$PORT
   ```

3. Alternatively, if you prefer to run with `python main.py`, ensure the app reads the `$PORT` env var (this repo's `main.py` supports that after the update).

4. Configure a reverse proxy (nginx) for static files and SSL as needed.

## Future Enhancements

- Email notifications for task assignments
- File upload for task submissions
- Advanced reporting and analytics
- Calendar integration
- Mobile app development
- API endpoints for external integrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please create an issue in the project repository.

---

**Built with ❤️ using Flask**