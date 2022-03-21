from django.contrib import admin
from .models import User, Product, RefLink, Payment, Announcement


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'last_name', 'birth_day', 'balance')
    list_display_links = ('id', 'first_name')
    search_fields = ('id', 'user_id', 'first_name')
    list_editable = ('balance',)
    list_filter = ('id',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('id', 'name', 'price')
    list_editable = ('price',)
    list_filter = ('price',)

class RefLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link', 'date')
    list_display_links = ('name',)
    search_fields = ('name', 'date')
    list_editable = ('description',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'products', 'status', 'date')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'date')

class AnnouncmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RefLink, RefLinkAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Announcement, AnnouncmentAdmin)