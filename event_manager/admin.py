from django.contrib import admin
from .models import Event, Ticket

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass