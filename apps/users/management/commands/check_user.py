"""
Management command to check and manage user authentication issues.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.users.models import LoginHistory

User = get_user_model()


class Command(BaseCommand):
    help = 'Check user authentication status and troubleshoot login issues'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username or email to check')
        parser.add_argument(
            '--fix-active',
            action='store_true',
            help='Activate the user account'
        )
        parser.add_argument(
            '--fix-verify',
            action='store_true',
            help='Mark user email as verified'
        )
        parser.add_argument(
            '--reset-password',
            type=str,
            help='Set a new password for the user'
        )
        parser.add_argument(
            '--show-logins',
            action='store_true',
            help='Show recent login attempts'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            # Try to find user by username or email
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ User "{username}" not found in database')
                )
                self.stdout.write('\nAvailable users:')
                for u in User.objects.all()[:10]:
                    self.stdout.write(f'  • {u.username} ({u.email})')
                raise CommandError(f'User "{username}" not found')

        # Display user info
        self.stdout.write(self.style.SUCCESS(f'\n✓ User Found: {user.username}'))
        self.stdout.write(f'  Email: {user.email}')
        self.stdout.write(f'  Active: {self.style.SUCCESS("✓") if user.is_active else self.style.ERROR("✗")} {user.is_active}')
        self.stdout.write(f'  Verified: {self.style.SUCCESS("✓") if user.is_verified else self.style.ERROR("✗")} {user.is_verified}')
        self.stdout.write(f'  Superuser: {user.is_superuser}')
        self.stdout.write(f'  Last Login: {user.last_login or "Never"}')
        self.stdout.write(f'  Login Count: {user.login_count}')

        # Show recent failed logins
        if options['show_logins']:
            self.stdout.write('\nRecent login attempts:')
            recent_logins = LoginHistory.objects.filter(user=user).order_by('-created_at')[:10]
            if recent_logins.exists():
                for login in recent_logins:
                    status = self.style.SUCCESS('✓ SUCCESS') if login.was_successful else self.style.ERROR('✗ FAILED')
                    reason = f' ({login.failure_reason})' if login.failure_reason else ''
                    self.stdout.write(f'  {login.created_at} - {status}{reason}')
            else:
                self.stdout.write('  No login history found')

        # Apply fixes if requested
        if options['fix_active'] and not user.is_active:
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS('\n✓ User activated!'))

        if options['fix_verify'] and not user.is_verified:
            user.is_verified = True
            user.email_verified_at = None
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ User email verified!'))

        if options['reset_password']:
            user.set_password(options['reset_password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Password reset successfully!'))
            self.stdout.write(f'  New password: {options["reset_password"]}')

        # Test authentication
        from django.contrib.auth import authenticate
        from apps.users.backends import EmailOrUsernameBackend
        
        test_password = options.get('reset_password', 'test')
        self.stdout.write('\nAuthentication test:')
        
        if options.get('reset_password'):
            # Test 1: Direct password check
            direct_check = user.check_password(test_password)
            self.stdout.write(f'  Direct password check: {self.style.SUCCESS("✓ PASS") if direct_check else self.style.ERROR("✗ FAIL")}')
            
            # Test 2: Django authenticate() function
            auth_test = authenticate(username=user.username, password=test_password)
            self.stdout.write(f'  Django authenticate(): {self.style.SUCCESS("✓ PASS") if auth_test else self.style.ERROR("✗ FAIL")}')
            
            # Test 3: Direct backend call
            backend = EmailOrUsernameBackend()
            backend_auth = backend.authenticate(None, username=user.username, password=test_password)
            self.stdout.write(f'  Backend direct call: {self.style.SUCCESS("✓ PASS") if backend_auth else self.style.ERROR("✗ FAIL")}')
            
            if backend_auth and not auth_test:
                self.stdout.write(self.style.WARNING('\n⚠️ Backend works but Django authenticate() failed!'))
                self.stdout.write('  Check AUTHENTICATION_BACKENDS setting in settings.py')
        else:
            self.stdout.write('  (Run with --reset-password to test authentication)')
