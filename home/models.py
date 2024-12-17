from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class ChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField(blank=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} {self.object_id} at {self.timestamp}"
class Airport(models.Model):
    name = models.CharField(max_length=300,default='AIIAP Lahore')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.name} "
    
class Employee(models.Model):
    DEPARTMENT_CHOICES = (
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             related_name='employees')
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    salary = models.PositiveIntegerField()
    
class EqptTypes(models.Model):
    type = models.CharField(max_length=400)
    image = models.ImageField(upload_to ='uploads/',blank=True) # file will be uploaded to MEDIA_ROOT / uploads 

class PlaceInstallaion(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT,)
    sector = models.CharField(max_length=200)
    duty_point = models.CharField(max_length=400,blank=True)
    call_sign = models.CharField(max_length=200,blank=True)
    equipment_issued = models.ManyToManyField('Equipment',blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.call_sign} "
    
class Staff(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT,)
    name = models.CharField(max_length=100)
    force_no = models.CharField(max_length=10)
    dob = models.DateField(max_length=200,blank=True)
    cnic=models.PositiveBigIntegerField(unique=True)
    date_of_joining_asf = models.DateField(max_length=200,blank=True)
    date_of_joining_current_station = models.DateField(max_length=200,blank=True)
    image = models.ImageField(upload_to ='uploads/',blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_by', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Check if it's a new instance
            user = User.objects.create_user(
                username=self.cnic,  # Use cnic as username
                password='08408'  # Set a default password
            )
            self.user = user
        super().save(*args, **kwargs)

@receiver(post_save, sender=Staff)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.save()  # To trigger the save method and create the User
    def __str__(self):
        return f"{self.force_no}  {self.name} "
class EqptStatus(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.title} "
class EqptType(models.Model):
    title = models.CharField(max_length=300)
    features=models.TextField(blank=True)
    def __str__(self):
        return f"{self.title}"
class Equipment(models.Model):
    stp={
        'p':'Pass','f':'Fail'
    }
    airport = models.ForeignKey(Airport, on_delete=models.PROTECT,)
    manufacturer = models.CharField(max_length=200,blank=True)
    made_in = models.CharField(max_length=100,blank=True)
    serial_no = models.CharField(max_length=200,blank=True)
    type = models.ForeignKey(EqptType, on_delete=models.RESTRICT,blank=True)
    title = models.CharField(max_length=200,blank=True)
    model = models.CharField(max_length=500,blank=True)
    status = models.ForeignKey(EqptStatus, on_delete=models.RESTRICT,blank=True)
    stp_status = models.CharField(max_length=200,choices=stp,default=stp['p'])
    date_of_manufacturing = models.DateField(blank=True)
    place_of_installation = models.ForeignKey(PlaceInstallaion,on_delete=models.RESTRICT,blank=True)
    remarks = models.TextField(max_length=400,blank=True) #IC1, received from=
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.airport} - {self.serial_no} - {self.type} - {self.title} - {self.status}"
    class Meta:
        permissions = [
            ("can_add_equipment", "Can add equipment"),
            ("can_change_equipment", "Can change equipment"),
            ("can_delete_equipment", "Can delete equipment"),
            ("can_view_equipment", "Can view equipment"),
        ]
    
class NewModel(models.Model):
    title = models.CharField(max_length=200)
# Create your models here.
from  django.utils.timezone import now


class Repair(models.Model):
    title = models.CharField(max_length=400)
    date=models.DateTimeField(default=now())
    repair_type = models.CharField(max_length=300, choices=[('pm','Preventative Maintenance'),('cm','Corrective Maintenance')],default='pm')
    staff = models.ManyToManyField(Staff)
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE,)
    description = models.TextField(blank=True)   # Complete description
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} - {self.staff} - {self.equipment}"
