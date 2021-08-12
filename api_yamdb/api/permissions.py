from django.contrib import admin
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            if request.user.is_authenticated:
                return request.user.role == 'admin'
            return False    
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = ('admin',)
        return request.user.role in role or obj.author == request.user


class FullAcessOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = ('moderator', 'admin',)
        return request.user.role in role or obj.author == request.user
