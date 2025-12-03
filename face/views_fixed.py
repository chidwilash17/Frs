@csrf_exempt
def api_start_session(request):
    """API endpoint for faculty/admin to start an attendance session"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Authentication required'})
        
        # Check if user has admin or faculty role
        if not (request.user.role and request.user.role.name.lower() in ['admin', 'faculty']):
            return JsonResponse({'success': False, 'message': 'Administrator or Faculty privileges required'})
        
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({'success': False, 'message': 'Session ID is required'})
        
        try:
            # Get the original session to copy its properties
            original_session = AttendanceSession.objects.get(id=session_id)
            
            # Check if faculty is authorized to start this session
            if request.user.role.name.lower() == 'faculty' and original_session.faculty != request.user:
                return JsonResponse({'success': False, 'message': 'You are not authorized to start this session'})
            
            # Create a new session instance with the same properties
            new_session = AttendanceSession.objects.create(
                name=original_session.name,
                location_constraint=original_session.location_constraint,
                start_time=timezone.now(),
                end_time=timezone.now() + (original_session.end_time - original_session.start_time),
                is_active=True,
                faculty=original_session.faculty
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Session "{new_session.name}" started successfully',
                'session_id': new_session.id
            })
            
        except AttendanceSession.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Session not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error starting session: {str(e)}'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

@csrf_exempt
def api_stop_session(request):
    """API endpoint for faculty/admin to stop an attendance session"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Authentication required'})
        
        # Check if user has admin or faculty role
        if not (request.user.role and request.user.role.name.lower() in ['admin', 'faculty']):
            return JsonResponse({'success': False, 'message': 'Administrator or Faculty privileges required'})
        
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({'success': False, 'message': 'Session ID is required'})
        
        try:
            session = AttendanceSession.objects.get(id=session_id)
            
            # Check if faculty is authorized to stop this session
            if request.user.role.name.lower() == 'faculty' and session.faculty != request.user:
                return JsonResponse({'success': False, 'message': 'You are not authorized to stop this session'})
            
            session.is_active = False
            session.end_time = timezone.now()  # Set end time when stopping session
            session.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'Session "{session.name}" stopped successfully',
                'session_id': session.id
            })
            
        except AttendanceSession.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Session not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error stopping session: {str(e)}'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})