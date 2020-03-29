import logging
import types

from rest_framework.authtoken.models import Token
from rest_framework import permissions

from knuvote_app.enums import ResponseMsg
from knuvote_app.models import Category, User

logger = logging.getLogger(__name__)

class IsOwnerOreadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creatorId == request.user

class IsOwner():
    def has_object_permission(request, obj):
        try:
            userId = Token.objects.get(key=request.headers['Authorization']).user_id
        except Token.DoesNotExist:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Category):
            return str(obj.creator) == User.objects.get(id=userId).email
        else: return obj.id == userId

class IsAuthenticated():
    def has_object_permission(request):
        try:
            token = Token.objects.get(key=request.headers['Authorization'])
        except Token.DoesNotExist:
            return False
        return True
