from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Department, Company, Employee


@receiver(post_save, sender=Department)
@receiver(pre_delete, sender=Department)
def update_company_department_num(sender, instance, **kwargs):
    company = instance.company
    company.departments_num = company.departments.count()
    company.save()


@receiver(post_save, sender=Employee)
@receiver(pre_delete, sender=Employee)
def update_department_employee_num(sender, instance, **kwargs):
    department = instance.department
    department.employees_num = department.employees.count()
    department.save()

    company = instance.company
    company.employees_num = company.employees.count()
    company.save()
