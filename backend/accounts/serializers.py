from rest_framework import serializers
from .models import Company, Department, Employee, User
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['departments_num', 'employees_num']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_company(**user_data)
        return Company.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        if user_data:
            user_instance = instance.user
            if 'password' in user_data:
                user_instance.set_password(user_data['password'])
            user_instance.save()
        company_name = validated_data.get('company_name')
        if company_name:
            instance.company_name =company_name
        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # company = CompanySerializer()
    company_id = serializers.IntegerField()
    company = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['employees_num']

    def create(self, validated_data):
        try:
            # company = Company.objects.get(id=validated_data.pop('company')['id'])
            company = Company.objects.get(id=validated_data.pop('company_id'))
            user_data = validated_data.pop('user')
            user = User.objects.create_department(**user_data)
            return Department.objects.create(user=user, company=company, **validated_data)
        except Company.DoesNotExist:
            raise serializers.ValidationError("This Company does  not exist")

    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        if user_data:
            user_instance = instance.user
            if 'password' in user_data:
                user_instance.set_password(user_data['password'])
            user_instance.save()
        dep_name = validated_data.get('department_name')
        if dep_name:
            instance.department_name = dep_name
        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company_id = serializers.IntegerField()
    company = serializers.CharField(source='company.company_name', read_only=True)
    department_id = serializers.IntegerField()
    department = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['days_employed']

    def create(self, validated_data):
        try:
            dep = Department.objects.get(company__id=validated_data['company_id'], id=validated_data.pop('department_id'))
            company = Company.objects.get(id=validated_data.pop('company_id'))
            user_data = validated_data.pop('user')
            user = User.objects.create_employee(**user_data)
            return Employee.objects.create(user=user, department=dep, company=company, **validated_data)
        except Department.DoesNotExist:
            raise serializers.ValidationError("The department must be in the company's departments")

    def update(self, instance, validated_data):
        company_id = validated_data.get('company_id')
        dep_id = validated_data.get('department_id')
        if company_id and instance.company.id != company_id:
            try:
                dep = Department.objects.get(company__id=company_id, id=dep_id)
                company = Company.objects.get(id=company_id)
                instance.company = company
                instance.department = dep
                instance.save()
            except Department.DoesNotExist:
                raise serializers.ValidationError("The department must be in the company's departments")

        if dep_id and instance.department.id != dep_id:
            try:
                dep = Department.objects.get(company__id=instance.company.id, id=dep_id)
                instance.department = dep
                instance.save()
            except Department.DoesNotExist:
                raise serializers.ValidationError("The department must be in the company's departments")

        user_data = validated_data.pop('user')
        if user_data:
            user_instance = instance.user
            print(user_instance)
            print(user_data)
            if 'password' in user_data:
                instance.user.set_password(user_data['password'])
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
