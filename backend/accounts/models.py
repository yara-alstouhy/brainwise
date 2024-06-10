from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
# from django.db.models.signals import post_save, pre_delete
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.
from django.dispatch import receiver


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_company(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'Company Manger')
        return self._create_user(username, email, password, **extra_fields)

    def create_department(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'Department Manger')
        return self._create_user(username, email, password, **extra_fields)

    def create_employee(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'Employee')
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    objects = UserManager()

    def __str__(self):
        return self.username + " " + self.role


# phone = PhoneNumberField(region="EG")

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    departments_num = models.IntegerField(default=0)
    employees_num = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name


class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    department_name = models.CharField(max_length=255)
    employees_num = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name

    def clean(self):
        if not self.company:
            raise ValidationError('Department must be associated with a company.')


class Employee(models.Model):
    status = [
        ('application_received', 'Application Received'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('hired', 'Hired'),
        ('not_accepted', 'Not Accepted'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    employee_status = models.CharField(max_length=50, choices=status)
    employee_name = models.CharField(max_length=255)
    # email_address = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    mobile_number = PhoneNumberField(region="EG")
    address = models.TextField()
    designation = models.CharField(max_length=255)
    hired_on = models.DateField(null=True, blank=True)
    days_employed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.employee_name

    def clean(self):
        if self.hired_on and self.hired_on > date.today():
            raise ValidationError('Hired on date cannot be in the future.')

    @property
    def calc_days_employed(self):
        if self.hired_on:
            return (date.today() - self.hired_on).days
        return None

    def save(self, *args, **kwargs):
        self.days_employed = self.calc_days_employed
        super().save(*args, **kwargs)


