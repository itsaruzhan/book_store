from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Categories)
admin.site.register(BookReturnedRecord)
admin.site.register(BookRating)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Login)
from .models import BookRating
class CartAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    pass