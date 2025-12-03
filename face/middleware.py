from django.shortcuts import redirect
from django.contrib import messages
import re

class RoleBasedAccessMiddleware:
    """
    Simplified middleware for access control
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that are always accessible
        always_accessible = [
            '/login/',
            '/logout/',
            '/django-admin/',
            '/admin/',  # Django's built-in admin
            '/static/',
            '/media/',
            '/favicon.ico',
            '^$',  # Home page
        ]
        
        # Check if the path is always accessible
        requested_path = request.path
        is_always_accessible = any(
            re.match(path, requested_path) or requested_path.startswith(path)
            for path in always_accessible
        )
        
        # If path is always accessible, allow access
        if is_always_accessible:
            response = self.get_response(request)
            return response
        
        # If user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            # Don't redirect for API endpoints
            if requested_path.startswith('/api/'):
                response = self.get_response(request)
                return response
            return redirect('face:login')
        
        # For authenticated users, allow access to most pages
        response = self.get_response(request)
        return response

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response["X-Frame-Options"] = "DENY"
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(self), camera=(self)"
        
        return response

class RequestTimingMiddleware:
    """
    Middleware to log request processing time
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        # Log slow requests (more than 1 second)
        if duration > 1.0:
            print(f"Slow request: {request.path} took {duration:.2f}s")
        
        return response