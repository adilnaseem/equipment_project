from django.contrib import admin
from . import models
admin.site.register(models.Equipment)
admin.site.register(models.Staff)
admin.site.register(models.Repair)

admin.site.register(models.PlaceInstallaion)

admin.site.register(models.EqptType)
admin.site.register(models.Employee)
admin.site.register(models.EqptStatus)
admin.site.register(models.Airport)
@admin.register(models.ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'object_id', 'action', 'timestamp')
    list_filter = ('model_name', 'action', 'timestamp')
    search_fields = ('user__username', 'model_name', 'object_id')
# Register your models here.
