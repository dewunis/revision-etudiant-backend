from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Autorise l'accès en lecture et en écriture au propriétaire et au staff.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  
        # Vérifie si l'utilisateur est le propriétaire de l'objet
        return request.user.is_staff or obj.pk == request.user.pk
    
class IsProfileOwnerOrReadOnly(BasePermission):
    """
    Permet a un utilisateur de ne créé de profile que pour lui uniquement.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  
        # Si user_id n'est pas forni on laisse place a la validation de base
        if request.data.get('user_id') :
            # Si un entier n'est pas forni on laisse place a la validation de base
            if not request.data.get('user_id').isdigit():
                return True
            return request.user.pk == int(request.data.get('user_id'))
        return True