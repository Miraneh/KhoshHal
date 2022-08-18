from django.contrib import admin
from .models import Counselor
# Register your models here.


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ["get_first_name", "get_last_name", "specialty", "ME_number", "medial_information", "verified"]

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  # Allows column order sorting
    get_first_name.short_description = 'First Name'  # Renames column head

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'  # Allows column order sorting
    get_last_name.short_description = 'Last Name'  # Renames column head