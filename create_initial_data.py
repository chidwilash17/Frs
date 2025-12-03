import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frs.settings')
django.setup()

from face.models import Role, User

def create_initial_data():
    # Create roles
    roles_data = [
        {'name': 'admin', 'description': 'System Administrator'},
        {'name': 'hod', 'description': 'Head of Department'},
        {'name': 'faculty', 'description': 'Faculty Member'},
        {'name': 'principal', 'description': 'Principal'},
        {'name': 'student', 'description': 'Student'},
    ]
    
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            name=role_data['name'],
            defaults={'description': role_data['description']}
        )
        if created:
            print(f"Created role: {role.name}")
        else:
            print(f"Role already exists: {role.name}")
    
    # Create superuser
    if not User.objects.filter(roll_number='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            roll_number='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        admin_role = Role.objects.get(name='admin')
        admin_user.role = admin_role
        admin_user.save()
        print("Created superuser: admin")
    else:
        print("Superuser already exists")

if __name__ == '__main__':
    create_initial_data()