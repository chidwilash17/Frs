from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    """Model representing user roles"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    """Custom user model with roll number as username"""
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    face_encoding = models.TextField(blank=True, null=True)  # Store face encoding as string
    face_image = models.TextField(blank=True, null=True)  # Store face image as base64 string
    is_active = models.BooleanField(default=True)
    
    # New fields for student year, department, and level
    LEVEL_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'roll_number'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.roll_number} - {self.get_full_name()}"

class LocationConstraint(models.Model):
    """Model for defining location boundaries for attendance"""
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    radius = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)  # in meters
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class AttendanceSession(models.Model):
    """Model for attendance sessions"""
    name = models.CharField(max_length=100)
    location_constraint = models.ForeignKey(LocationConstraint, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='faculty_sessions')
    target_year = models.CharField(max_length=1, choices=User.YEAR_CHOICES, blank=True, null=True)  # Add target year field
    level = models.CharField(max_length=2, choices=User.LEVEL_CHOICES, blank=True, null=True)  # Add level field
    department = models.CharField(max_length=100, blank=True, null=True)  # Add department field
    
    def __str__(self):
        return f"{self.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class AttendanceRecord(models.Model):
    """Model for individual attendance records"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    verification_method = models.CharField(
        max_length=20,
        choices=[
            ('face', 'Face Recognition'),
            ('manual', 'Manual Verification')
        ],
        default='face'
    )
    
    class Meta:
        unique_together = ('user', 'session')
    
    def __str__(self):
        return f"{self.user.roll_number} - {self.session.name} - {self.timestamp}"

class MonthlyReport(models.Model):
    """Model for storing monthly attendance reports"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    total_sessions = models.IntegerField(default=0)
    attended_sessions = models.IntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'month')
    
    def __str__(self):
        return f"{self.user.roll_number} - {self.month.strftime('%B %Y')} - {self.attendance_percentage}%"