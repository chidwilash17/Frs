from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from ...models import AttendanceSession, AttendanceRecord, MonthlyReport
from ...utils import send_monthly_report_email
from datetime import datetime, timedelta
import calendar

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate monthly attendance reports and send emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            type=str,
            help='Month to generate reports for (YYYY-MM format)',
        )

    def handle(self, *args, **options):
        # Determine the month to generate reports for
        if options['month']:
            try:
                year, month = map(int, options['month'].split('-'))
                report_date = timezone.datetime(year, month, 1)
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid month format. Use YYYY-MM')
                )
                return
        else:
            # Default to previous month
            today = timezone.now().date()
            first_day_current_month = today.replace(day=1)
            report_date = first_day_current_month - timedelta(days=1)
            report_date = report_date.replace(day=1)
        
        self.stdout.write(
            f'Generating monthly reports for {report_date.strftime("%B %Y")}'
        )
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            # Get all sessions in the report month
            start_date = report_date.replace(day=1)
            last_day = calendar.monthrange(report_date.year, report_date.month)[1]
            end_date = report_date.replace(day=last_day) + timedelta(days=1)
            
            # Get sessions in the month
            sessions = AttendanceSession.objects.filter(
                start_time__gte=start_date,
                start_time__lt=end_date
            )
            
            total_sessions = sessions.count()
            
            # Get attendance records for the user in these sessions
            attended_sessions = AttendanceRecord.objects.filter(
                user=user,
                session__in=sessions
            ).count()
            
            # Calculate attendance percentage
            if total_sessions > 0:
                attendance_percentage = (attended_sessions / total_sessions) * 100
            else:
                attendance_percentage = 0.0
            
            # Create or update the monthly report
            report, created = MonthlyReport.objects.update_or_create(
                user=user,
                month=report_date,
                defaults={
                    'total_sessions': total_sessions,
                    'attended_sessions': attended_sessions,
                    'attendance_percentage': attendance_percentage
                }
            )
            
            # Send email report
            if send_monthly_report_email(user, report):
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully sent report to {user.email}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'Failed to send report to {user.email}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('Monthly reports generation completed')
        )