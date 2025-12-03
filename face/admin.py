from django.contrib import admin
from .models import User, Role, LocationConstraint, AttendanceSession, AttendanceRecord, MonthlyReport

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('roll_number', 'email', 'first_name', 'last_name')

@admin.register(LocationConstraint)
class LocationConstraintAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'radius', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_constraint', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'location_constraint')
    search_fields = ('name',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'timestamp', 'verification_method')
    list_filter = ('session', 'verification_method')
    search_fields = ('user__roll_number', 'session__name')

@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'attended_sessions', 'total_sessions', 'attendance_percentage')
    list_filter = ('month',)
    search_fields = ('user__roll_number',)