from rest_framework import permissions



class IsActiveTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.role == "teacher"


class IsStudent(permissions.BasePermission):
    """
    Allows access only to authenticated users with student role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


def is_valid_iranian_national_id(input: str) -> bool:
    if not input.isdigit() or len(input) != 10:
        return False

    digits = [int(ch) for ch in input]
    check = digits[9]
    s = sum(digits[i] * (10 - i) for i in range(9)) % 11

    return (s < 2 and check == s) or (s >= 2 and check + s == 11)



