from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.sender) or (request.user == obj.reciever)


class IsReciever(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciever
