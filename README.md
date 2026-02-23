# Student Task & Attendance Management System

A Flask-based web application designed to manage student tasks and attendance using role-based access control.
The system allows administrators to manage students, tasks, and attendance, while students can track their assigned tasks and attendance records.
***A web-based system where students can view tasks and attendance, and admins manage students, tasks, and attendance.***

---

## 🚀 Live Demo
🔗https://student-task-attendance-management-system.onrender.com
 
---

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

### Key Highlights
- Role-based authentication for Admin and Student users
- Secure login without displaying demo credentials
- Clean and modular Flask project structure
- Simple and user-friendly interface
