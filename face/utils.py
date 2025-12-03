import base64
import numpy as np
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import cv2
import os
from datetime import datetime, date
import json
import face_recognition

def encode_face(image):
    """
    Encode a face image into a feature vector using the face_recognition library
    """
    try:
        # Convert image to RGB if it's in BGR format (OpenCV uses BGR)
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            # If grayscale, convert to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Detect faces in the image using HOG model (faster) first
        face_locations = face_recognition.face_locations(rgb_image, model="hog")
        
        # If no faces found with HOG, try CNN model (more accurate but slower)
        if not face_locations:
            face_locations = face_recognition.face_locations(rgb_image, model="cnn")
        
        # If still no faces found, try with upsampling
        if not face_locations:
            face_locations = face_recognition.face_locations(rgb_image, number_of_times_to_upsample=2)
        
        # If no faces detected, return None
        if not face_locations:
            print("No faces detected in the image")
            return None
        
        # Use the first detected face
        top, right, bottom, left = face_locations[0]
        
        # Extract face encoding
        face_encodings = face_recognition.face_encodings(rgb_image, [face_locations[0]])
        
        if not face_encodings:
            print("Could not encode face")
            return None
            
        encoding = face_encodings[0]
        print(f"Face encoding shape: {encoding.shape}")
        return encoding
        
    except Exception as e:
        print(f"Error encoding face: {e}")
        import traceback
        traceback.print_exc()
        return None

def base64_to_image(base64_string):
    """
    Convert base64 string to image
    """
    try:
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
            
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is not None:
            print(f"Image shape: {image.shape}")
        else:
            print("Failed to decode image")
        
        return image
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_faces(known_encoding, unknown_encoding, tolerance=0.4):
    """
    Compare two face encodings using the face_recognition library with stricter tolerance
    """
    try:
        # Check if encodings are valid
        if known_encoding is None or unknown_encoding is None:
            print("One or both encodings are None")
            return False
            
        # Check if encodings have the same shape
        if known_encoding.shape != unknown_encoding.shape:
            print(f"Encoding shape mismatch: known {known_encoding.shape}, unknown {unknown_encoding.shape}")
            return False
            
        # Use face_recognition's compare_faces function with stricter tolerance
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=tolerance)
        
        match_result = matches[0] if matches else False
        print(f"Face comparison result: {match_result} with tolerance {tolerance}")
        
        # Also calculate the distance for additional verification
        face_distances = face_recognition.face_distance([known_encoding], unknown_encoding)
        distance = face_distances[0] if len(face_distances) > 0 else 1.0
        print(f"Face distance: {distance}")
        
        # Even if compare_faces says True, double-check with distance
        if match_result and distance > tolerance:
            print(f"Warning: compare_faces returned True but distance {distance} > tolerance {tolerance}")
            return False
            
        return match_result
    except Exception as e:
        print(f"Error comparing faces: {e}")
        import traceback
        traceback.print_exc()
        return False

def is_live_capture(image):
    """
    Enhanced liveness detection to prevent spoofing with static images
    """
    try:
        # Check if image is valid
        if image is None or image.size == 0:
            return False
            
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # 1. Check image quality - static images often have different characteristics
        # Calculate Laplacian variance to measure image blur
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 50:  # Very blurry images are suspicious
            print(f"Image too blurry (variance: {laplacian_var}), likely not live")
            return False
            
        # 2. Detect faces first
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            print("No faces detected for liveness check")
            return False
            
        # 3. Check for eye regions and potential blink detection
        # This is a simplified check - in production, you'd want more sophisticated blink detection
        face_landmarks_list = face_recognition.face_landmarks(image)
        if not face_landmarks_list:
            print("No face landmarks detected")
            return False
            
        # 4. Check for multiple faces (photos of screens often show multiple faces)
        if len(face_locations) > 1:
            print(f"Multiple faces detected ({len(face_locations)}), likely not live")
            return False
            
        # 5. Check image metadata patterns that suggest it's a photo of a screen
        # This is a heuristic check - screen photos often have specific color patterns
        # Check color distribution
        if len(image.shape) == 3:
            # Calculate color variance
            color_variance = np.var(image, axis=(0, 1))
            avg_color_variance = np.mean(color_variance)
            if avg_color_variance < 100:  # Very low color variance suggests screen photo
                print(f"Low color variance ({avg_color_variance}), likely screen photo")
                return False
                
        # 6. Check for Moire patterns (common in photos of screens)
        # Apply FFT to detect repetitive patterns
        try:
            # Convert to grayscale if needed
            if len(gray.shape) == 3:
                gray_check = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
            else:
                gray_check = gray
                
            # Apply FFT
            f = np.fft.fft2(gray_check)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
            
            # Check for high frequency patterns
            center = (gray_check.shape[0] // 2, gray_check.shape[1] // 2)
            radius = min(center) // 4
            mask = np.zeros_like(magnitude_spectrum)
            cv2.circle(mask, center, radius, 1, -1)
            high_freq_energy = np.sum(magnitude_spectrum * (1 - mask))
            
            # If high frequency energy is too high, it might be a screen photo
            if high_freq_energy > 1000000:  # Threshold determined empirically
                print(f"High frequency energy ({high_freq_energy}), likely screen photo")
                return False
        except Exception as fft_error:
            print(f"FFT check failed: {fft_error}")
            # Continue with other checks even if FFT fails
            
        # 7. Check for unnatural brightness patterns
        mean_brightness = np.mean(gray)
        if mean_brightness < 30 or mean_brightness > 220:
            print(f"Unnatural brightness ({mean_brightness}), potentially not live")
            return False
            
        # If all checks pass, consider it a live capture
        print("Liveness check passed")
        return True
    except Exception as e:
        print(f"Error in liveness detection: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_attendance_email(user, attendance_record):
    """
    Send attendance confirmation email to user
    """
    try:
        subject = 'Attendance Marked Successfully'
        message = f'''
        Hello {user.get_full_name() or user.roll_number},
        
        Your attendance has been successfully marked for the session.
        
        Timestamp: {attendance_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        
        Thank you for using the Face Recognition Attendance System.
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending attendance email: {e}")
        return False

def send_user_details_email(user, action, password=None):
    """
    Send user details email to user when created or updated by HOD
    
    Args:
        user: User object containing user details
        action: String indicating action ('created' or 'updated')
        password: Password for newly created users (optional)
    """
    try:
        subject = f'Account {action.capitalize()} - Face Recognition Attendance System'
        
        # Build user details message
        message = f'''
Hello {user.get_full_name() or user.roll_number},

Your account has been {action} by the Head of Department in the Face Recognition Attendance System.

Account Details:
Roll Number: {user.roll_number}
First Name: {user.first_name}
Last Name: {user.last_name}
Email: {user.email}
Role: {user.role.name if user.role else 'Not assigned'}
Level: {user.level or 'Not specified'}
Year: {user.year or 'Not specified'}
Department: {user.department or 'Not specified'}
Status: {'Active' if user.is_active else 'Inactive'}
'''
        
        # Include password only for new accounts
        if action == 'created' and password:
            message += f'Password: {password}\n\n'
            message += 'Please change your password after first login.\n\n'
        
        message += '''
If you have any questions, please contact your Head of Department.

Thank you for using the Face Recognition Attendance System.
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending user details email: {e}")
        return False


def send_attendance_report_email(user, report_date, attendance_data):
    """
    Send attendance report email to user for a specific date
    
    Args:
        user: User object to send email to
        report_date: Date for which the report is generated
        attendance_data: List of attendance records for sessions on that date
    """
    try:
        # Check if user already received an email today
        if user_already_received_email_today(user.id, report_date):
            print(f"User {user.email} already received an attendance report today. Skipping.")
            return True  # Return True to indicate success (no need to send)
        
        subject = f'Attendance Report - {report_date.strftime("%Y-%m-%d")} - {user.department}'
        
        # Find the latest session based on session start time (not attendance timestamp)
        latest_session_time = None
        latest_session_date = None
        if attendance_data:
            for record in attendance_data:
                # Use session_time instead of attendance timestamp
                session_time_str = record['session_time']  # This is already in the right format
                if session_time_str:
                    # For latest session, we just need the latest session_time
                    if latest_session_time is None or session_time_str > latest_session_time:
                        latest_session_time = session_time_str
                        # Extract date from session_time
                        try:
                            # session_time is in format "YYYY-MM-DD HH:MM"
                            from datetime import datetime
                            dt = datetime.strptime(session_time_str, "%Y-%m-%d %H:%M")
                            latest_session_date = dt.date()
                        except ValueError:
                            pass  # Handle parsing error
        
        # Build attendance report message
        message = f'''
Hello {user.get_full_name() or user.roll_number},

This is your attendance report for {report_date.strftime("%Y-%m-%d")} in the {user.department} department.

'''
        
        # Add latest session information if available
        if latest_session_time and latest_session_date:
            
            message += f"Latest session start date: {latest_session_date}\n\n"
        
        message += "Session Attendance Details:\n"
        
        if attendance_data:
            for record in attendance_data:
                status = "Attended" if record['attended'] else "Absent"
                timestamp = record['timestamp'] if record['timestamp'] else "N/A"
                # Show only the attendance timestamp, not the session time
                message += f"- {record['session_name']}: {status}"
                if record['attended']:
                    message += f" - Marked at {timestamp}"
                message += "\n"
        else:
            message += "No sessions were conducted on this date.\n"
        
        message += '''
If you have any questions about your attendance, please contact your Head of Department.

Thank you for using the Face Recognition Attendance System.
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        # Record that we sent an email to this user today
        record_email_sent(user.id, report_date)
        
        return True
    except Exception as e:
        print(f"Error sending attendance report email to {user.email}: {e}")
        return False

def user_already_received_email_today(user_id, report_date):
    """Check if user already received an email today"""
    try:
        # Create a simple tracking file
        tracking_file = os.path.join(os.path.dirname(__file__), 'email_tracking.json')
        
        # If file doesn't exist, user hasn't received an email
        if not os.path.exists(tracking_file):
            return False
            
        # Read the tracking data
        with open(tracking_file, 'r') as f:
            tracking_data = json.load(f)
        
        # Check if user has an entry for today
        user_key = str(user_id)
        today_str = report_date.strftime("%Y-%m-%d")
        
        if user_key in tracking_data and tracking_data[user_key] == today_str:
            return True
            
        return False
    except Exception as e:
        print(f"Error checking email tracking: {e}")
        return False  # If there's an error, we'll send the email to be safe

def record_email_sent(user_id, report_date):
    """Record that an email was sent to a user today"""
    try:
        # Create a simple tracking file
        tracking_file = os.path.join(os.path.dirname(__file__), 'email_tracking.json')
        
        # Read existing data or create empty dict
        if os.path.exists(tracking_file):
            with open(tracking_file, 'r') as f:
                tracking_data = json.load(f)
        else:
            tracking_data = {}
        
        # Update the tracking data
        user_key = str(user_id)
        today_str = report_date.strftime("%Y-%m-%d")
        tracking_data[user_key] = today_str
        
        # Write back to file
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f)
    except Exception as e:
        print(f"Error recording email sent: {e}")