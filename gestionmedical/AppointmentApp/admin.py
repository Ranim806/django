from django.contrib import admin
from .models import Appointment


@admin.action(description="make them confirmed")
def confirmed_appointment(model,req,queryset):
    queryset.update(status='CONFIRMED')

@admin.register(Appointment)
class appointmentAdminUser(admin.ModelAdmin):
    list_display = ['reason', 'status', 'duration_minutes', 'appointment_date']
    list_filter = ['status', 'appointment_date']
    list_editable = ['status', 'duration_minutes']

    search_fields = ['reason', 'status']
    ordering = ['appointment_date']

   
    fieldsets = (
        ('Description', {
            'fields': ('reason', 'status', 'prescription')
        }),
        ('Date et duree', {
            'fields': ('appointment_date', 'duration_minutes')
        }),
        ('Patients / Doctors', {
            'fields': ('doctor', 'patient')
        }),
        ('Planification', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']
    