#!/usr/bin/env python
"""
Consolidated System Creation Script

This script consolidates all school management system creation and setup functions
into a single executable file. It combines role creation, permission assignment,
multi-tenancy setup, analytics setup, and other initialization tasks.

Usage:
    python create.py

Features:
    - Automatically runs makemigrations and migrate
    - Executes all populate/seed management commands
    - Prompts for superuser creation
    - Comprehensive error handling and logging

Requirements:
    - Django environment must be properly configured
    - Database should be set up and available
    - All required apps must be installed

Author: Nexus Intelligence School Management System
"""

import os
import sys
import getpass
import django
from django.conf import settings
from django.core.management import call_command, execute_from_command_line
from django.contrib.auth import get_user_model
from pathlib import Path
import subprocess
import time
import re

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.development')
django.setup()

User = get_user_model()


class SystemCreator:
    """Handles all system creation and setup tasks."""

    def __init__(self):
        self.created = 0
        self.updated = 0
        self.success_commands = []
        self.failed_commands = []
        self.fixed_seed_staff_roles = False

    def log_success(self, message):
        """Log a success message."""
        print(f"✓ {message}")

    def log_info(self, message):
        """Log an info message."""
        print(f"ℹ {message}")

    def log_warning(self, message):
        """Log a warning message."""
        print(f"⚠ {message}")

    def log_error(self, message):
        """Log an error message."""
        print(f"✗ {message}")

    def run_command(self, command_name, *args, **kwargs):
        """Run a Django management command with error handling."""
        try:
            self.log_info(f'Running {command_name}...')
            call_command(command_name, *args, **kwargs)
            self.log_success(f'Successfully executed {command_name}')
            self.success_commands.append(command_name)
            return True
        except Exception as e:
            self.log_error(f'Failed to execute {command_name}: {e}')
            self.failed_commands.append((command_name, str(e)))
            return False

    def run_migrations(self):
        """Run makemigrations and migrate."""
        self.log_info("Running database migrations...")
        
        # Run makemigrations for all apps
        try:
            self.run_command('makemigrations')
        except SystemExit:
            self.log_info("No changes detected or makemigrations exited normally")
        except Exception as e:
            self.log_error(f"Error running makemigrations: {e}")
            return False
        
        # Run migrate
        if self.run_command('migrate'):
            self.log_success("Database migrations completed successfully")
            return True
        else:
            self.log_error("Database migrations failed")
            return False

    def fix_seed_staff_roles(self):
        """Fix the seed_staff_roles command by running it after institution is created."""
        if self.fixed_seed_staff_roles:
            return True
            
        self.log_info("Fixing seed_staff_roles command...")
        try:
            # First, create a default institution if it doesn't exist
            from apps.core.models import Institution
            from apps.users.models import Role
            
            # Check if default institution exists
            default_institution = Institution.objects.filter(code='DEFAULT').first()
            if not default_institution:
                self.log_info("Creating default institution...")
                default_institution = Institution.objects.create(
                    name='Default School',
                    code='DEFAULT',
                    short_name='Default',
                    description='Default institution',
                    institution_type='high_school',
                    ownership_type='private',
                    is_active=True,
                    allows_online_enrollment=True,
                    requires_parent_approval=True
                )
                self.log_success(f"Created default institution: {default_institution.name}")
            
            # Now run the seed_staff_roles command again
            self.log_info("Running seed_staff_roles again...")
            from apps.users.models import Role as UserRole
            from django.db import transaction
            
            with transaction.atomic():
                # Define staff roles with their display names and descriptions
                staff_roles_data = [
                    {
                        'role_type': UserRole.RoleType.SUPER_ADMIN,
                        'name': 'Super Administrator',
                        'description': 'Full system access and control',
                        'hierarchy_level': 100,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.ADMIN,
                        'name': 'Administrator',
                        'description': 'Administrative access to school management',
                        'hierarchy_level': 90,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.PRINCIPAL,
                        'name': 'Principal',
                        'description': 'School principal with oversight of all operations',
                        'hierarchy_level': 85,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.DEPARTMENT_HEAD,
                        'name': 'Department Head',
                        'description': 'Head of an academic department',
                        'hierarchy_level': 70,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.COUNSELOR,
                        'name': 'School Counselor',
                        'description': 'Student counseling and guidance',
                        'hierarchy_level': 60,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.TEACHER,
                        'name': 'Teacher',
                        'description': 'Classroom teacher',
                        'hierarchy_level': 50,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.ACCOUNTANT,
                        'name': 'Accountant',
                        'description': 'Financial management and accounting',
                        'hierarchy_level': 45,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.LIBRARIAN,
                        'name': 'Librarian',
                        'description': 'Library management and services',
                        'hierarchy_level': 40,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.DRIVER,
                        'name': 'Driver',
                        'description': 'School transport driver',
                        'hierarchy_level': 30,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.SUPPORT,
                        'name': 'Support Staff',
                        'description': 'General support staff',
                        'hierarchy_level': 25,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.TRANSPORT_MANAGER,
                        'name': 'Transport Manager',
                        'description': 'Management of school transportation',
                        'hierarchy_level': 55,
                        'institution': default_institution,
                    },
                    {
                        'role_type': UserRole.RoleType.HOSTEL_WARDEN,
                        'name': 'Hostel Warden',
                        'description': 'Management of student hostel facilities',
                        'hierarchy_level': 50,
                        'institution': default_institution,
                    },
                ]

                created_count = 0
                updated_count = 0

                for role_data in staff_roles_data:
                    role, created = UserRole.objects.get_or_create(
                        role_type=role_data['role_type'],
                        institution=default_institution,
                        defaults={
                            'name': role_data['name'],
                            'description': role_data['description'],
                            'hierarchy_level': role_data['hierarchy_level'],
                            'is_system_role': True,
                            'status': 'active',
                        }
                    )

                    if created:
                        created_count += 1
                        self.log_success(f'Created role: {role.name}')
                    else:
                        # Update existing role if needed
                        updated = False
                        if role.name != role_data['name']:
                            role.name = role_data['name']
                            updated = True
                        if role.description != role_data['description']:
                            role.description = role_data['description']
                            updated = True
                        if role.hierarchy_level != role_data['hierarchy_level']:
                            role.hierarchy_level = role_data['hierarchy_level']
                            updated = True
                        if role.status != 'active':
                            role.status = 'active'
                            updated = True

                        if updated:
                            role.save()
                            updated_count += 1
                            self.log_warning(f'Updated role: {role.name}')
                
                self.log_success(f'Created {created_count} roles, updated {updated_count} roles')
                self.fixed_seed_staff_roles = True
                return True
                
        except Exception as e:
            self.log_error(f'Error fixing seed_staff_roles: {e}')
            import traceback
            traceback.print_exc()
            return False

    def run_all_setup_commands(self):
        """Run all setup commands in proper order."""
        # First fix the seed_staff_roles issue
        if not self.fix_seed_staff_roles():
            self.log_error("Failed to fix seed_staff_roles")
            return
        
        # Define the order of commands to run
        setup_commands = [
            # First: Core setup commands (seed_staff_roles already fixed)
            ('setup_multitenancy', 'Setting up multi-tenancy...'),
            ('create_system_kpis', 'Creating system KPIs...'),
            ('create_system_reports', 'Creating system reports...'),
            
            # Second: Populate data commands
            ('populate_exam_types', 'Populating exam types...'),
            ('populate_faqs', 'Populating FAQs...'),
            ('populate_legal_documents', 'Populating legal documents...'),
            
            # Third: Permission and user management (run after roles are created)
            ('assign_role_permissions', 'Assigning role permissions...'),
            ('assign_transport_permissions', 'Assigning transport permissions...'),
            ('sync_permissions', 'Synchronizing user permissions...'),
            ('map_unmapped_users', 'Mapping unmapped users...'),
            
            # Fourth: Data collection (optional - can be skipped if desired)
            ('collect_system_metrics', 'Collecting system metrics...'),
        ]
        
        # Execute commands
        for command_name, description in setup_commands:
            self.log_info(description)
            self.run_command(command_name)
        
        # Create institution (optional - prompt user)
        if self.prompt_yes_no("Do you want to create a new institution? (y/n): "):
            self.create_institution_interactive()
        
        # Run any additional populate_* commands found
        self.run_additional_populate_commands()

    def run_additional_populate_commands(self):
        """Run any additional populate_* commands that weren't explicitly listed."""
        from django.core.management import get_commands
        
        all_commands = get_commands()
        populate_commands = [cmd for cmd in all_commands.keys() if cmd.startswith('populate_')]
        
        # Exclude already run commands
        already_run = ['populate_exam_types', 'populate_faqs', 'populate_legal_documents']
        new_commands = [cmd for cmd in populate_commands if cmd not in already_run]
        
        if new_commands:
            self.log_info(f"Found {len(new_commands)} additional populate commands")
            for command_name in new_commands:
                self.run_command(command_name)

    def prompt_yes_no(self, question):
        """Prompt user for yes/no input."""
        while True:
            response = input(f"{question} ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please answer 'y' or 'n'")

    def create_institution_interactive(self):
        """Interactively create a new institution."""
        self.log_info("\nCreating a new institution...")
        
        try:
            # Get institution details from user
            name = input("Institution name: ").strip()
            if not name:
                self.log_warning("Institution creation skipped - no name provided")
                return
            
            code = input("Institution code (for subdomain): ").strip()
            if not code:
                self.log_warning("Institution creation skipped - no code provided")
                return
            
            admin_email = input("Admin email address: ").strip()
            if not admin_email:
                self.log_warning("Institution creation skipped - no admin email provided")
                return
            
            # Optional fields
            description = input("Description (optional): ").strip()
            phone = input("Phone number (optional): ").strip()
            address = input("Address (optional): ").strip()
            
            # Build command arguments
            args = [name, code, f'--admin_email={admin_email}']
            
            if description:
                args.append(f'--description={description}')
            if phone:
                args.append(f'--phone={phone}')
            if address:
                args.append(f'--address={address}')
            
            # Ask if this should be default institution
            if self.prompt_yes_no("Set as default institution? (y/n): "):
                args.append('--set_default')
            
            # Run the create_institution command
            self.log_info(f"Creating institution: {name} ({code})")
            self.run_command('create_institution', *args)
            
        except KeyboardInterrupt:
            self.log_warning("Institution creation cancelled by user")
        except Exception as e:
            self.log_error(f"Error creating institution: {e}")

    def create_superuser_interactive(self):
        """Interactively create a superuser."""
        self.log_info("\nCreating superuser account...")
        
        try:
            # Check if superuser already exists
            if User.objects.filter(is_superuser=True).exists():
                self.log_warning("Superuser already exists.")
                if not self.prompt_yes_no("Do you want to create another superuser? (y/n): "):
                    return None
            
            # Get credentials from user
            print("\nPlease enter superuser credentials:")
            
            # Check if User model has username field
            has_username_field = hasattr(User, 'username')
            
            if has_username_field:
                username = input("Username: ").strip()
                if not username:
                    self.log_error("Username cannot be empty")
                    return None
            else:
                # If no username field, we'll use email as identifier
                username = None
            
            email = input("Email address: ").strip()
            
            # Validate email
            if not email or '@' not in email:
                self.log_error("Invalid email address")
                if self.prompt_yes_no("Try again? (y/n): "):
                    return self.create_superuser_interactive()
                return None
            
            # Get password (twice for confirmation)
            while True:
                password = getpass.getpass("Password: ").strip()
                confirm_password = getpass.getpass("Confirm password: ").strip()
                
                if not password:
                    print("Password cannot be empty")
                    if not self.prompt_yes_no("Try again? (y/n): "):
                        return None
                    continue
                
                if password != confirm_password:
                    print("Passwords do not match")
                    if not self.prompt_yes_no("Try again? (y/n): "):
                        return None
                else:
                    break
            
            # Create superuser
            try:
                if has_username_field and username:
                    # User model has username field
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                else:
                    # User model uses email as username
                    user = User.objects.create_superuser(
                        email=email,
                        password=password
                    )
                    
                self.log_success(f"Superuser created successfully: {email}")
                return user
                
            except Exception as e:
                self.log_error(f"Error creating superuser: {e}")
                if self.prompt_yes_no("Try again? (y/n): "):
                    return self.create_superuser_interactive()
                
        except KeyboardInterrupt:
            self.log_warning("Superuser creation cancelled by user")
            return None
        except Exception as e:
            self.log_error(f"Unexpected error: {e}")
            return None

    def run_all_setup(self):
        """Run all setup functions in proper order."""
        print("=" * 60)
        print(" SCHOOL MANAGEMENT SYSTEM - COMPLETE SETUP ")
        print("=" * 60)
        print()
        
        try:
            # Step 1: Run migrations
            self.log_info("Step 1: Running database migrations...")
            if not self.run_migrations():
                self.log_error("Setup aborted due to migration failures")
                return False
            
            print()
            print("-" * 60)
            
            # Step 2: Run all setup commands
            self.log_info("Step 2: Running system setup commands...")
            self.run_all_setup_commands()
            
            print()
            print("-" * 60)
            
            # Step 3: Create superuser
            self.log_info("Step 3: Creating superuser...")
            self.create_superuser_interactive()
            
            # Step 4: Display summary
            self.display_summary()
            
            return True
            
        except Exception as e:
            self.log_error(f"Setup failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def display_summary(self):
        """Display setup summary."""
        print()
        print("=" * 60)
        self.log_success("SYSTEM SETUP COMPLETE!")
        print("=" * 60)
        
        if self.success_commands:
            print(f"\nSuccessfully executed {len(self.success_commands)} commands:")
            for cmd in self.success_commands:
                print(f"  ✓ {cmd}")
        
        if self.failed_commands:
            print(f"\nFailed to execute {len(self.failed_commands)} commands:")
            for cmd, error in self.failed_commands:
                print(f"  ✗ {cmd}: {error[:50]}...")
        
        # Display helpful next steps
        print("\nNEXT STEPS:")
        print("1. Start the development server: python manage.py runserver")
        print("2. Access the admin panel at: http://localhost:8000/admin/")
        print("3. Review system settings")
        print("4. Add additional users and data as needed")
        print("5. Test the system functionality")
        
        if self.failed_commands:
            print("\n⚠  Some commands failed. You may need to run them manually.")
            print("   Check the error messages above for details.")


def main():
    """Main execution function."""
    try:
        creator = SystemCreator()
        
        # Confirm user wants to proceed
        print("This script will:")
        print("1. Run database migrations (makemigrations and migrate)")
        print("2. Execute all system setup commands")
        print("3. Create a superuser account")
        print("4. Set up the complete school management system")
        print()
        print("WARNING: This will modify your database.")
        print("Make sure you have backups if needed.")
        print()
        
        response = input("Do you want to proceed? (y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Setup cancelled.")
            return 0
        
        # Run setup
        start_time = time.time()
        success = creator.run_all_setup()
        end_time = time.time()
        
        if success:
            print(f"\n🎉 Setup completed successfully in {end_time - start_time:.2f} seconds!")
            print("\nTo start the development server, run:")
            print("    python manage.py runserver")
            return 0
        else:
            print(f"\n❌ Setup failed or was incomplete.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Setup failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())