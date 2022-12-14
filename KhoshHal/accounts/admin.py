from django.contrib import admin
from .models import Counselor, Patient, Reservation, Appointment

# Register your models here.

admin.site.register(Appointment)
admin.site.register(Reservation)


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ["get_username", "get_first_name", "get_last_name", "meeting_link", "specialty", "ME_number", "medical_information",
                    "verified", "get_email"]

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.admin_order_field = 'user__first_name'  # Allows column order sorting
    get_first_name.short_description = 'First Name'  # Renames column head

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.admin_order_field = 'user__last_name'  # Allows column order sorting
    get_last_name.short_description = 'Last Name'  # Renames column head

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'  # Allows column order sorting
    get_email.short_description = 'Email'  # Renames column head



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["get_username", "get_first_name", "get_last_name", "get_email"]

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user__username'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.admin_order_field = 'user__first_name'  # Allows column order sorting
    get_first_name.short_description = 'First Name'  # Renames column head

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.admin_order_field = 'user__last_name'  # Allows column order sorting
    get_last_name.short_description = 'Last Name'  # Renames column head

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'  # Allows column order sorting
    get_email.short_description = 'Email'  # Renames column head
