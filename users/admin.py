from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# models.py에 있는 모든 것을 import한다.

# Register your models here.


@admin.register(
    models.User
)  # 왼쪽에 있는 것이 decorator인데 admin.site.register(models.User, CustomUserAdmin) 와 같다.
# models.py에 있는 User 객체를 가져온다.


class CustomerUserAdmin(UserAdmin):

    """ Custom User Admin """

    # UserAdmin.fieldsets와 내가 만든 새로운 필드값을 합쳐서 구현해준다.
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )


# admin pannel에 표기되는 요소들을 하나씩 수정해준다.
# class CustomerUserAdmin(admin.ModelAdmin):
# list_display = ("username", "email", "gender", "language", "currency", "superhost")
# list_filter = ("language", "currency", "superhost")

