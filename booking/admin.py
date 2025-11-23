from django.contrib import admin
from .models import Service, TimeSlot, Reservation


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("service", "start", "end", "is_active")
    list_filter = ("service", "is_active")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "slot", "status", "created_at")
    list_filter = ("status", "service")
