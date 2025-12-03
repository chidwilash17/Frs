from django.urls import path
from . import views

app_name = 'face'

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Unified dashboard
    path('dashboard/', views.unified_dashboard, name='unified_dashboard'),
    
    # Admin dashboard
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # HOD dashboard
    path('dashboard/hod/', views.hod_dashboard, name='hod_dashboard'),
    
    # Faculty dashboard
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    
    # Principal dashboard
    path('dashboard/principal/', views.principal_dashboard, name='principal_dashboard'),
    
    # Attendance URLs
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/process/', views.process_attendance, name='process_attendance'),
    path('attendance/register-face/', views.register_face, name='register_face'),
    path('attendance/view/', views.view_attendance, name='view_attendance'),
    
    # Location constraint URLs
    path('location/constraint/', views.location_constraint, name='location_constraint'),
    path('location/set/', views.set_location_constraint, name='set_location_constraint'),
    path('location/constraint/delete/<int:location_id>/', views.delete_location_constraint, name='delete_location_constraint'),
    
    # Session management URLs
    path('session/manage/', views.manage_sessions, name='manage_sessions'),
    path('session/create/', views.create_session, name='create_session'),
    path('session/start/<int:session_id>/', views.start_session, name='start_session'),
    path('session/stop/<int:session_id>/', views.stop_session, name='stop_session'),
    path('session/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    
    # API endpoints for Flutter app
    path('api/login/', views.api_login, name='api_login'),
    path('api/register-face/', views.api_register_face, name='api_register_face'),
    path('api/mark-attendance/', views.api_mark_attendance, name='api_mark_attendance'),
    path('api/user-info/', views.api_user_info, name='api_user_info'),
    
    # New API endpoints for enhanced features
    path('api/create-session/', views.api_create_session, name='api_create_session'),
    path('api/start-session/', views.api_start_session, name='api_start_session'),
    path('api/stop-session/', views.api_stop_session, name='api_stop_session'),
    path('api/delete-session/<int:session_id>/', views.api_delete_session, name='api_delete_session'),
    path('api/create-location-constraint/', views.api_create_location_constraint, name='api_create_location_constraint'),
    path('api/delete-location-constraint/<int:location_id>/', views.api_delete_location_constraint, name='api_delete_location_constraint'),
    path('api/get-active-session/', views.api_get_active_session, name='api_get_active_session'),
    path('api/get-all-sessions/', views.api_get_all_sessions, name='api_get_all_sessions'),
    path('api/get-active-sessions/', views.api_get_active_sessions, name='api_get_active_sessions'),
    path('api/get-all-attendance-records/', views.api_get_all_attendance_records, name='api_get_all_attendance_records'),
    path('api/get-user-attendance/', views.api_get_user_attendance, name='api_get_user_attendance'),
    path('api/get-admin-dashboard-stats/', views.api_get_admin_dashboard_stats, name='api_get_admin_dashboard_stats'),
    path('api/get-location-constraints/', views.api_get_location_constraints, name='api_get_location_constraints'),
    
    # New API endpoints for profile and user management
    path('api/get-user-profile/', views.api_get_user_profile, name='api_get_user_profile'),
    path('api/get-all-users/', views.api_get_all_users, name='api_get_all_users'),
    path('api/get-all-roles/', views.api_get_all_roles, name='api_get_all_roles'),
    path('api/create-user/', views.api_create_user, name='api_create_user'),
    path('api/update-user/<int:user_id>/', views.api_update_user, name='api_update_user'),
    path('api/delete-user/<int:user_id>/', views.api_delete_user, name='api_delete_user'),
    path('api/get-registered-faces/', views.api_get_registered_faces, name='api_get_registered_faces'),
    path('api/delete-user-face/<int:user_id>/', views.api_delete_user_face, name='api_delete_user_face'),
    path('api/calculate-monthly-attendance/', views.api_calculate_monthly_attendance, name='api_calculate_monthly_attendance'),
    path('api/get-user-monthly-reports/', views.api_get_user_monthly_reports, name='api_get_user_monthly_reports'),
    path('api/change-password/', views.api_change_password, name='api_change_password'),

    # New API endpoints for HOD functionality
    path('api/get-hod-dashboard-stats/', views.api_get_hod_dashboard_stats, name='api_get_hod_dashboard_stats'),
    path('api/get-faculty-members/', views.api_get_faculty_members, name='api_get_faculty_members'),
    path('api/get-faculty-attendance-records/', views.api_get_faculty_attendance_records, name='api_get_faculty_attendance_records'),
    path('api/hod/filtered-registered-faces/', views.api_get_hod_filtered_registered_faces, name='api_get_hod_filtered_registered_faces'),
    path('api/hod/send-attendance-report/', views.api_send_hod_attendance_report, name='api_send_hod_attendance_report'),

    # New API endpoints for Faculty functionality
    path('api/get-faculty-sessions/', views.api_get_faculty_sessions, name='api_get_faculty_sessions'),
    path('api/faculty/location-constraints/', views.api_faculty_get_location_constraints, name='api_faculty_get_location_constraints'),
    path('api/faculty/create-location-constraint/', views.api_faculty_create_location_constraint, name='api_faculty_create_location_constraint'),
    path('api/faculty/sessions/', views.api_faculty_sessions, name='api_faculty_sessions'),
    path('api/faculty/sessions/<int:session_id>/start/', views.api_faculty_start_session, name='api_faculty_start_session'),
    path('api/faculty/sessions/<int:session_id>/stop/', views.api_faculty_stop_session, name='api_faculty_stop_session'),
    path('api/faculty/sessions/<int:session_id>/delete/', views.api_faculty_delete_session, name='api_faculty_delete_session'),
    path('api/faculty/sessions/<int:session_id>/attendance/', views.api_get_faculty_session_attendance, name='api_get_faculty_session_attendance'),
    path('api/faculty/sessions-with-attendance/', views.api_get_faculty_sessions_with_attendance, name='api_get_faculty_sessions_with_attendance'),
    path('api/faculty/daily-attendance/', views.api_get_faculty_daily_attendance, name='api_get_faculty_daily_attendance'),
    path('api/faculty/filtered-daily-attendance/', views.api_get_filtered_faculty_daily_attendance, name='api_get_filtered_faculty_daily_attendance'),
    path('api/faculty/active-session/', views.api_get_active_session, name='api_faculty_get_active_session'),
    path('api/faculty/attendance-records/', views.api_get_faculty_attendance_records, name='api_faculty_get_attendance_records'),
    path('api/faculty/attendance-records/<int:faculty_id>/', views.api_get_faculty_attendance_records_by_faculty, name='api_get_faculty_attendance_records_by_faculty'),
    path('api/get-faculty-attendance-records/<int:faculty_id>/', views.api_get_faculty_attendance_records_by_faculty, name='api_get_faculty_attendance_records_by_faculty_old'),
    path('api/faculty/mark-attendance/', views.api_faculty_mark_attendance, name='api_faculty_mark_attendance'),
    path('api/faculty/students/', views.api_get_students_for_faculty, name='api_get_students_for_faculty'),
    path('api/hod/filtered-sessions/', views.api_get_hod_filtered_sessions, name='api_get_hod_filtered_sessions'),
    path('api/hod/users/', views.api_get_hod_users, name='api_get_hod_users'),
]