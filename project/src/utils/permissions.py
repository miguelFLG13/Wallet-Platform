from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Permission to only allow commerces
    """

    def has_permission(self, request, view):
        if request.user.polymorphic_ctype.model == 'customer':
            return True
        return False
