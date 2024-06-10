from django.urls import path

from .views import *

urlpatterns = [
    # path('test/', EmployeeViewSet.as_view()),
    path('login/', jwtlogin.as_view()),
    path('company/', CompanyListCreateAPIView.as_view()),
    path('company/<int:pk>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    path('department/', DepartmentListCreateAPIView.as_view()),
    path('department/<int:pk>/', DepartmentRetrieveUpdateDestroyAPIView.as_view()),
    path('employee/', EmployeeListCreateAPIView.as_view()),
    path('employee/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view())
]
