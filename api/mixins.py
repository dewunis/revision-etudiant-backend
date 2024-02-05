from .permissions import IsStaffPermissions
from rest_framework.permissions import IsAdminUser

class IsStaffPermissionsMixin():
    permission_classes = [IsAdminUser,IsStaffPermissions]