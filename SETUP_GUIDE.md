# Quick Setup Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Access the Application
- Open your browser and go to: **http://localhost:5000**
- Login with admin credentials:
  - **Username**: `admin`
  - **Password**: `admin123`

## 📋 What You Can Do

### As Admin:
1. **Create Student Accounts** - Add new students to the system
2. **Assign Tasks** - Create and assign tasks with priorities and due dates
3. **Mark Attendance** - Track daily attendance for all students
4. **View Dashboard** - Monitor system statistics and recent activities

### As Student:
1. **View Tasks** - See all assigned tasks and their status
2. **Update Progress** - Change task status (pending → in progress → completed)
3. **Check Attendance** - View personal attendance records and statistics
4. **Dashboard Overview** - See personal statistics and recent activities

## 🔧 Verification
Run the verification script to ensure everything is set up correctly:
```bash
python verify_setup.py
```

## 📁 Project Structure
```
student-management-system/
├── app.py                    # Main Flask application
├── models.py                 # Database models (User, Task, Attendance)
├── forms.py                  # Form validation
├── config.py                 # Configuration settings
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── static/css/style.css      # Custom styling
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── auth/login.html      # Login page
│   ├── admin/               # Admin templates
│   └── student/             # Student templates
└── README.md                # Detailed documentation
```

## 🎯 Key Features
- **Role-based Authentication** (Admin/Student)
- **Task Management** with status tracking
- **Attendance Management** with monthly views
- **Responsive Design** for mobile and desktop
- **Clean Dashboard** with statistics
- **Form Validation** and error handling
- **Flash Messages** for user feedback

## 🔒 Security Features
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Role-based access control

## 📊 Database Models
- **User**: Handles admin and student accounts
- **Task**: Task assignment and tracking
- **Attendance**: Daily attendance records

## 🎨 UI/UX Features
- Modern, clean interface
- Responsive grid layouts
- Interactive dashboards
- Status badges and progress indicators
- Mobile-friendly design

---
**Ready to use! 🎉**