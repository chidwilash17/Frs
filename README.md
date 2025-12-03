# Face Recognition Attendance System

A comprehensive Django-based attendance system with facial recognition, location constraints, and role-based dashboards.

## Features

### Core Functionality
1. **Facial Recognition Attendance**
   - Face registration and verification
   - Camera-based attendance marking
   - Face encoding storage and comparison

2. **Location-Based Constraints**
   - GPS location verification
   - Radius-based attendance restrictions
   - Admin location setup

3. **Role-Based Dashboards**
   - Admin dashboard with user/session management
   - HOD, Faculty, and Principal dashboards
   - Student dashboard for attendance marking

4. **Automated Reporting**
   - Email notifications for attendance
   - Monthly attendance percentage reports
   - Attendance analytics

### Security Features
- Role-based access control
- CSRF protection
- Session management
- Face anti-spoofing (in Flutter app)

## Technical Details

- **Framework:** Django 4.2
- **Database:** SQLite3
- **Facial Recognition:** face_recognition library
- **Frontend:** Bootstrap 5 (Web) / Flutter (Mobile)
- **Authentication:** Custom roll number based system

## Setup Instructions

### Django Web Application

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Load initial data** (optional):
   ```bash
   python create_initial_data.py
   ```

5. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Flutter Mobile Application

For mobile access, a Flutter app is available in the `flutter_attendance` directory:

1. **Install Flutter dependencies**:
   ```bash
   cd flutter_attendance
   flutter pub get
   ```

2. **Update server URL** in `lib/services/auth_service.dart`

3. **Run the app**:
   ```bash
   flutter run
   ```

See `FLUTTER_INTEGRATION_GUIDE.md` for detailed integration instructions.

## Default Credentials

- **Admin:** roll_number: `admin`, password: `admin123`
- **HOD:** roll_number: `hod`, password: `hod123`
- **Faculty:** roll_number: `faculty`, password: `faculty123`
- **Principal:** roll_number: `principal`, password: `principal123`
- **Student:** roll_number: `student`, password: `student123`

## URLs

- **Home:** http://127.0.0.1:8000/
- **Login:** http://127.0.0.1:8000/login/
- **Unified Dashboard:** http://127.0.0.1:8000/dashboard/
- **Django Admin:** http://127.0.0.1:8000/django-admin/

## Key Components

### Models
- `User`: Custom user model with roll number
- `Role`: User roles (Admin, HOD, Faculty, Principal, Student)
- `LocationConstraint`: GPS boundaries for attendance
- `AttendanceSession`: Attendance sessions managed by Admin
- `AttendanceRecord`: Individual attendance records
- `MonthlyReport`: Monthly attendance reports

### Views
- Authentication views (login, logout)
- Dashboard views for all roles
- Attendance management views
- Location constraint management
- User management views

### Security
- Custom authentication backend
- Role-based access middleware
- Security headers middleware
- Request timing middleware

## Mobile App Features (Flutter)

The Flutter mobile app provides enhanced functionality:

1. **Face Registration**
   - Mobile camera integration
   - Real-time face detection
   - Anti-spoofing measures

2. **Attendance Marking**
   - Face recognition verification
   - GPS location validation
   - Real-time attendance recording

3. **Security Enhancements**
   - Liveness detection
   - Photo/video spoofing prevention
   - Encrypted communication

See `FLUTTER_INTEGRATION_GUIDE.md` for complete mobile app documentation.

## Management Commands

### Generate Monthly Reports
```bash
python manage.py generate_monthly_reports
```

## Customization

### Adding New Roles
1. Create new role in Django admin
2. Add role-specific dashboard view
3. Update middleware for access control
4. Create role-specific templates

### Modifying Attendance Workflow
1. Update `AttendanceSession` model
2. Modify attendance processing logic
3. Adjust location constraint validation
4. Update email notification templates

## Troubleshooting

### Common Issues

1. **CSRF Verification Failed**
   - Add your domain to `CSRF_TRUSTED_ORIGINS` in settings.py
   - For ngrok: `CSRF_TRUSTED_ORIGINS = ['https://your-ngrok-url.ngrok.io']`

2. **No Module Named 'face_recognition'**
   - Install with: `pip install face-recognition`

3. **Database Lock Issues**
   - Close any database connections
   - Restart development server

## License

This project is for educational purposes. Please ensure compliance with privacy laws when using facial recognition technology.