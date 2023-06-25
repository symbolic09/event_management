from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    booking_start_datetime = models.DateTimeField()
    booking_end_datetime = models.DateTimeField()
    max_seat = models.IntegerField(default=10)
    available_seat = models.IntegerField(default=10)
    event_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.event_datetime.strftime('%d-%b-%Y @ %H:%M')}"
    
    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "booking_start_datetime": self.booking_start_datetime.strftime('%d-%b-%Y @ %H:%M'),
            "booking_end_datetime": self.booking_end_datetime.strftime('%d-%b-%Y @ %H:%M'),
            "max_seat": self.max_seat,
            "available_seat": self.available_seat,
            "event_datetime": self.event_datetime.strftime('%d-%b-%Y @ %H:%M'),
            "created_at": self.created_at.strftime('%d-%b-%Y @ %H:%M'),
            "updated_at": self.updated_at.strftime('%d-%b-%Y @ %H:%M')
        }

class Ticket(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_fields')
        ]

    def __str__(self):
        return f"{self.user.get_username()} - {self.event.name}"
    
    def as_dict(self):
        return {
            "event": self.event,
            "user": self.user,
            "booked_at": self.booked_at.strftime('%d-%b-%Y @ %H:%M'),
            "created_at": self.created_at.strftime('%d-%b-%Y @ %H:%M'),
            "updated_at": self.updated_at.strftime('%d-%b-%Y @ %H:%M')
        }