from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
import jwt
from .models import Department, Employee, Company


def getUser(request):
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        token = request.GET.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return True, payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        is_authenticated, user = getUser(request)
        return is_authenticated and request.user.role == 'employee'

    def has_object_permission(self, request, view, obj):
        is_authenticated, user = getUser(request)
        return is_authenticated and request.user == obj.user


class IsDepartmentManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'department'

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            return obj.department.user == request.user
        if isinstance(obj, Department):
            return obj.user == request.user
        if isinstance(obj, Company):
            return obj == request.user.company
        return False


class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'company'

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            return obj.company.user == request.user
        if isinstance(obj, Department):
            return obj.company.user == request.user
        if isinstance(obj, Company):
            return obj.user == request.user
        return False


class IsCompanyAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'company'

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if isinstance(obj, Employee):
            return obj.company.user == request.user
        if isinstance(obj, Department):
            return obj.company.user == request.user
        if isinstance(obj, Company):
            return obj.user == request.user
        return False

#
# class EmployeePermission(BasePermission):
#
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         return request.user.role.name == 'Employee' and view.action == 'view_employee_data'
#
#
# class DepartmentPermission(BasePermission):
#     """
#     Permission class for Department role.
#     """
#
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         user_role = request.user.role.name
#         allowed_actions = {
#             'add_employee': 'POST',
#             'edit_employee': 'PUT',
#             'delete_employee': 'DELETE',
#             'update_employee': 'PATCH',
#             'view_employee_data': 'GET',
#             'view_department_data': 'GET',
#         }
#         return user_role == 'Department' and view.action == allowed_actions.get(view.action)
#
#
# class CompanyPermission(BasePermission):
#
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         user_role = request.user.role.name
#         allowed_actions = {
#             'add_employee': 'POST',
#             'edit_employee': 'PUT',
#             'delete_employee': 'DELETE',
#             'update_employee': 'PATCH',
#             'view_employee_data': 'GET',
#             'view_department_data': 'GET',
#             'add_department': 'POST',
#             'edit_department': 'PUT',
#             'delete_department': 'DELETE',
#             'update_department': 'PATCH',
#             'view_company_data': 'GET',
#         }
#         return user_role == 'Company' and view.action == allowed_actions.get(view.action)
#
#
# class AdminPermission(BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role.name == 'admin'
