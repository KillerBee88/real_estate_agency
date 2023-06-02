from django.contrib import admin
from .models import Flat, Complaint, Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phonenumber', 'normalized_phonenumber')
    search_fields = ['full_name', 'phonenumber', 'normalized_phonenumber']


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ('address', 'price', 'new_building', 'construction_year', 'town')
    list_editable = ('new_building',)
    search_fields = ['town', 'address', 'owners__full_name']
    readonly_fields = ['created_at']
    list_filter = ('new_building', 'rooms_number', 'has_balcony')
    raw_id_fields = ('likes',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat', 'text')
    search_fields = ['user__username', 'flat__address', 'text']
    raw_id_fields = ('flat',)
