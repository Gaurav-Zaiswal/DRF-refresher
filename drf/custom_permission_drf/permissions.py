from email import message
from rest_framework import permissions

class ReadWriteUpdatePermission(permissions.BasePermission):
    """
    Let user to READ, WRITE, or UPDATE, but not DELETE the data.
    Nobody will be able to perform DELETE
    """
    message = "not authorized to delete"

    def has_permission(self, request, view):
        '''
        overall permission to the View
        just like IsAuthenticated, AllowAny etc.
        '''
        if request.method == "DELETE":
            return False
        return True


    def has_object_permission(self, request, view, obj):
        '''
        let only admin or the owner of the product modify/delete an object/product
        '''
        if request.method in ["DELETE", "PUT", "PATCH"]:
            if not obj.author == request.user:
                return False
            return True 
        return True