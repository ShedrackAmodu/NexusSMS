from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AuditLog



@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin interface for AuditLog model.
    """
    list_display = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp', 'user')
    search_fields = ('user__email', 'model_name', 'object_id', 'ip_address')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'details',
                      'ip_address', 'user_agent', 'timestamp', 'created_at', 'updated_at')
    date_hierarchy = 'timestamp'

    fieldsets = (
        (_('Audit Information'), {
            'fields': ('user', 'action', 'model_name', 'object_id', 'timestamp')
        }),
        (_('Technical Details'), {
            'fields': ('details', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        (_('System Metadata'), {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Prevent manual creation of audit logs."""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent modification of audit logs."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion only for superusers."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Deny access to school_admin users."""
        if self._user_has_school_admin_role(request.user):
            return False
        return super().has_view_permission(request, obj)

    def _user_has_school_admin_role(self, user):
        """Check if user has school_admin role."""
        if not user.is_authenticated:
            return False
        return user.user_roles.filter(
            role__role_type='school_admin',
            status='active'
        ).exists()
