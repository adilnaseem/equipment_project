from rest_framework import serializers
from . import models
class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EqptType
        fields = ['title', 'features']
        # ("serial_no", "type", "title", "s
class EquipmentSerializer(serializers.ModelSerializer):
    type = EquipmentTypeSerializer()
    class Meta:
        model = models.Equipment
        fields = '__all__'
        # ("serial_no", "type", "title", "status", "received_from", "date_of_installation", "description")

from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    department = serializers.ChoiceField(choices=Employee.DEPARTMENT_CHOICES)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'name', 'department', 'salary')