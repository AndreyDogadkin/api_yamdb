from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'is_superuser',
    )
    search_fields = (
        'username',
        'email',
    )
    empty_value_display = 'Не задано'
