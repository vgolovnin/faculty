from django.contrib import admin

from .models import Reservist, Category, Stage, Status, Department
admin.site.register(Reservist)
admin.site.register(Category)
admin.site.register(Stage)
admin.site.register(Status)
admin.site.register(Department)