from django.contrib import admin
from accounts.models import User,UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','role','is_active')
    ordering = ('-date_joined',)# this is tuple,so comma is must
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User,CustomAdmin)
admin.site.register(UserProfile)
