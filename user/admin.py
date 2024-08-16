from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    # Customize how the user model is displayed on the admin dashboard
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)  # Specify a valid field for ordering, such as 'email'

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
