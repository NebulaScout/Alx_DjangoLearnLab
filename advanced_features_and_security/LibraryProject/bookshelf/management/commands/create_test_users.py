from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from bookshelf.models import CustomUser, UserProfile
from datetime import date


class Command(BaseCommand):
    help = 'Create test users for permission testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing test users before creating new ones',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test users for permission testing...'))
        
        # Test users data
        test_users = [
            {
                'username': 'test_admin',
                'email': 'admin@test.com',
                'password': 'testpass123',
                'role': 'admin',
                'group': 'Admins',
                'first_name': 'Admin',
                'last_name': 'User'
            },
            {
                'username': 'test_editor',
                'email': 'editor@test.com',
                'password': 'testpass123',
                'role': 'librarian',
                'group': 'Editors',
                'first_name': 'Editor',
                'last_name': 'User'
            },
            {
                'username': 'test_viewer',
                'email': 'viewer@test.com',
                'password': 'testpass123',
                'role': 'member',
                'group': 'Viewers',
                'first_name': 'Viewer',
                'last_name': 'User'
            },
            {
                'username': 'test_nogroup',
                'email': 'nogroup@test.com',
                'password': 'testpass123',
                'role': 'member',
                'group': None,  # No group assigned
                'first_name': 'No Group',
                'last_name': 'User'
            }
        ]
        
        if options['reset']:
            # Delete existing test users
            test_usernames = [user['username'] for user in test_users]
            deleted_count = CustomUser.objects.filter(username__in=test_usernames).delete()[0]
            if deleted_count:
                self.stdout.write(f'Deleted {deleted_count} existing test users')
        
        created_users = []
        
        for user_data in test_users:
            try:
                # Check if user already exists
                if CustomUser.objects.filter(username=user_data['username']).exists():
                    self.stdout.write(
                        self.style.WARNING(f'User {user_data["username"]} already exists, skipping...')
                    )
                    continue
                
                # Create user
                user = CustomUser.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    date_of_birth=date(1990, 1, 1)  # Default date of birth
                )
                
                # Update user profile role
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.role = user_data['role']
                user_profile.save()
                
                # Assign to group if specified
                if user_data['group']:
                    try:
                        group = Group.objects.get(name=user_data['group'])
                        user.groups.add(group)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Created user: {user_data["username"]} → {user_data["group"]} group'
                            )
                        )
                    except Group.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'Group {user_data["group"]} does not exist')
                        )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created user: {user_data["username"]} → No group assigned'
                        )
                    )
                
                created_users.append(user_data)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating user {user_data["username"]}: {e}')
                )
        
        # Display summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('TEST USERS CREATED SUCCESSFULLY!'))
        self.stdout.write('=' * 60)
        
        if created_users:
            self.stdout.write('\n Test Users Summary:')
            self.stdout.write('-' * 40)
            
            for user_data in created_users:
                group_info = user_data['group'] if user_data['group'] else 'No Group'
                self.stdout.write(f"Username: {user_data['username']}")
                self.stdout.write(f"Password: {user_data['password']}")
                self.stdout.write(f"Role: {user_data['role']}")
                self.stdout.write(f"Group: {group_info}")
                self.stdout.write(f"Email: {user_data['email']}")
                self.stdout.write('-' * 40)
        
