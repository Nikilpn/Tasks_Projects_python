from django.contrib import admin
from blogapp.models import User,Blog,BlogReport,BlacklistedUser

# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(BlogReport)
admin.site.register(BlacklistedUser)