from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Permission to only allow customers
    """

    def has_permission(self, request, view):
        return request.user.is_customer()


class IsOwner(BasePermission):
    """
    Permission to only allow the owner of the wallet
    """

    def has_permission(self, request, view):
        if request.user.is_customer():
            return request.user.customer.wallets.filter(
                uuid=view.kwargs.get('uuid')
            ).exists()

        if request.user.is_commerce():
            return request.user.commerce.wallet.uuid == view.kwargs.get('uuid')

        return False
