from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions for the bookshelf app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all groups by clearing existing permissions first',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up user groups and permissions...'))
        
        # Define groups and their permissions
        groups_data = {
            'Editors': {
                'permissions': ['can_create', 'can_change', 'can_view'],
                'description': 'Can create, edit and view books'
            },
            'Viewers': {
                'permissions': ['can_view'],
                'description': 'Can only view books'
            },
            'Admins': {
                'permissions': ['can_create', 'can_change', 'can_delete', 'can_view'],
                'description': 'Full access to all book operations'
            }
        }

        # Get the Book content type
        try:
            book_content_type = ContentType.objects.get_for_model(Book)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting Book content type: {e}')
            )
            return

        for group_name, group_info in groups_data.items():
            # Create or get the group
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group {group_name} already exists')
                )
            
            # Clear existing permissions if reset flag is used or group is new
            if options['reset'] or created:
                group.permissions.clear()
                if options['reset']:
                    self.stdout.write(f'Cleared existing permissions for {group_name}')
            
            # Add permissions to the group
            permissions_added = 0
            for permission_codename in group_info['permissions']:
                try:
                    # Get the permission for the Book model
                    permission = Permission.objects.get(
                        codename=permission_codename,
                        content_type=book_content_type
                    )
                    group.permissions.add(permission)
                    permissions_added += 1
                    self.stdout.write(
                        f'Added permission: {permission.name}'
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Permission {permission_codename} does not exist for Book model'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error adding permission {permission_codename}: {e}'
                        )
                    )
            
            self.stdout.write(
                f'  Summary: {permissions_added}/{len(group_info["permissions"])} permissions added to {group_name}'
            )
            self.stdout.write(f'  Description: {group_info["description"]}\n')

        # Display summary
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Groups setup completed!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        # Show all groups and their permissions
        for group in Group.objects.all():
            self.stdout.write(f'\n📁 {group.name}:')
            permissions = group.permissions.all()
            if permissions:
                for perm in permissions:
                    self.stdout.write(f'   • {perm.name}')
            else:
                self.stdout.write('   • No permissions assigned')
                
        self.stdout.write(
            self.style.SUCCESS('\nYou can now assign users to these groups via Django admin or programmatically.')
        )