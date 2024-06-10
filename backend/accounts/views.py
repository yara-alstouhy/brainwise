import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, User
from .serializers import EmployeeSerializer, CompanySerializer, DepartmentSerializer
from .permissions import *


class jwtlogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('User not found!')

        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'role': user.role,
        }
        return response


# company
class CompanyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.kwargs['pk'])
        if company.employees_num == 0:
            user = company.user
            user.delete()
            return Response("delete successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("This company contains employee", status=status.HTTP_400_BAD_REQUEST)


# department
class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        auth, payload = getUser(self.request)
        if payload['role'] == 'Company Manger':
            return Department.objects.filter(company__user__id=payload['id'])
        else:
            return Department.objects.all()

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DepartmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    # def get_queryset(self):
    #     auth, payload = getUser(self.request)
    #     if payload['role'] == 'Company Manger':
    #         return Department.objects.filter(company__user__id=payload['id'])
    #     else:
    #         return Department.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        dep = Department.objects.get(id=self.kwargs['pk'])
        if dep.employees_num == 0:
            dep.user.delete()
            return Response("delete successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("This department contains employee", status=status.HTTP_400_BAD_REQUEST)


# EMPLOYEE

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer

    # permission_classes = [IsEmployee]
    def get_queryset(self):
        auth, payload = getUser(self.request)
        if payload['role'] == 'Department Manger':
            return Employee.objects.filter(department__user__id=payload['id'])
        elif payload['role'] == 'Company Manger':
            return Employee.objects.filter(company__user__id=payload['id'])
        else:
            return Employee.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # def get_queryset(self):
    #     auth, payload = getUser(self.request)
    #     if payload['role'] == 'Department Manger':
    #         return Employee.objects.get(department__user__id=payload['id'], id=self.kwargs['pk'])
    #     elif payload['role'] == 'Company Manger':
    #         return Employee.objects.get(company__user__id=payload['id'], id=self.kwargs['pk'])
    #     else:
    #         return Employee.objects.get(id=self.kwargs['pk'])

    # permission_classes = [IsEmployee]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        employee = Employee.objects.get(id=self.kwargs['pk'])
        employee.user.delete()
        return Response("delete successfully", status=status.HTTP_202_ACCEPTED)
