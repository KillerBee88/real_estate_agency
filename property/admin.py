from django.contrib import admin
from .models import Flat, Complaint


class FlatAdmin(admin.ModelAdmin):
    list_display = ('address', 'price', 'new_building', 'construction_year', 'town', 'owners_phonenumber', 'owner_normalized_phone')
    list_editable = ('new_building',)
    search_fields = ['town', 'address', 'owner']
    readonly_fields = ['created_at']
    list_filter = ('new_building', 'rooms_number', 'has_balcony')
    raw_id_fields = ('likes',)

admin.site.register(Flat, FlatAdmin)


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat', 'text')
    search_fields = ['user__username', 'flat__address', 'text']
    raw_id_fields = ('flat',)

admin.site.register(Complaint, ComplaintAdmin)