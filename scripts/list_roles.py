import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.users.models import Role

roles = Role.objects.all()
if not roles.exists():
    print("No roles found")
for r in roles:
    print(
        f"{r.id} | {r.name} | is_system_role={r.is_system_role} | status={getattr(r, 'status', None)} | perms={r.permissions.count()}"
    )
