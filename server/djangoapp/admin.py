from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel
# if i want to import all models
#from .models import *

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
    
# Register your models here.
#admin.site.register(CarMake)
#admin.site.register(CarModel)
# CarModelInline class
#class CarModelInline:
 #   pass


# CarModelAdmin class
#class CarModelAdminn(admin.ModelAdmin):
 #   list_display = ['title']
    
    
# CarMakeAdmin class with CarModelInline
# here i will updated at the end
#class CarMakeAdmin(admin.ModelAdmin):
#   inlines = [CarModelInline]
#   list_display = ('name', 'pub_date')
#  list_filter = ['pub_date']
# search_fields = ['name', 'description']


