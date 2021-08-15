from django.contrib import admin
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action is None:
            return True
        if view.action in ['create', 'destroy','update']:
            if request.user.is_authenticated:
                return request.user.role == 'admin'


class IsAdminOrReadOnlyPatch(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action is None:
            return True
        else:
            if request.user.is_authenticated:
                return request.user.role == 'admin'


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
