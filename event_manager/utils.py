from django.utils import timezone
from django.db import transaction
from http import HTTPStatus
from django.http import JsonResponse
import pytz

from .models import Event, Ticket
from .const import VALIDATE_EVENT_FIELDS
from event_manager import validators

from datetime import datetime


def get_live_events():
    now = timezone.now()
    return list(Event.objects.filter(booking_start_datetime__lte=now,
                                     booking_end_datetime__gte=now,
                                     available_seat__gte=1).order_by('event_datetime').values())


def get_all_events():
    return list(Event.objects.all().order_by('event_datetime').values())


def get_event_detail(event_id):
    try:
        return [Event.objects.get(id=event_id).as_dict()]
    except (Event.DoesNotExist, Event.MultipleObjectsReturned):
        return []


def validate_booking_info(data):
    return not Ticket.objects.filter(event__id=data.get('event')).exists() if 'event' in data.keys() else True


def get_tickets(user, ticket_id=None):
    tickets = Ticket.objects.filter(user=user)
    if ticket_id:
        return tickets.get(ticket_id).as_dict()
    else:
        return list(tickets.values())


@transaction.atomic
def try_booking_ticket(user, data):

    if Ticket.objects.filter(event__id=data.get('event')).exists():
        event = Event.objects.get(id=data.get('event'))
        if event.available_seat:
            event.available_seat -= 1
            event.save()
            Ticket.objects.create(event=event,
                                  user=user,
                                  booked_at=timezone.now())
            return "BOOKED"
        else:
            return "NO_SEAT_AVAILABLE"
    else:
        return "ALREADY_BOOKED"


def create_or_update_event(data):
    if validate_event_data(data):
        Event.objects.update_or_create(name=data.get('name'),
                                       description=data.get('description'),
                                       booking_start_datetime=convert_to_datetime(data.get('booking_start_datetime')),
                                       booking_end_datetime=convert_to_datetime(data.get('booking_end_datetime')),
                                       max_seat=data.get('max_seat'),
                                       available_seat=data.get('max_seat'),
                                       event_datetime=convert_to_datetime(data.get('event_datetime')))
        return "SUCCESS"
    else:
        return "VALIDATION_FAILED"


def convert_to_datetime(data):
    date_time = datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
    return date_time.astimezone(pytz.timezone('Asia/Kolkata'))


def validate_event_data(data):
    if all(key in data.keys() and getattr(validators, value)(data[key]) for key, value in VALIDATE_EVENT_FIELDS.items()):
        booking_start_datetime=convert_to_datetime(data.get('booking_start_datetime'))
        booking_end_datetime=convert_to_datetime(data.get('booking_end_datetime'))
        return booking_end_datetime > booking_start_datetime
    else:
        return False


def generate_response(content, is_success=True, http_status=HTTPStatus.OK):
    if is_success:
        status, result = ("SUCCESS", content) if isinstance(
            content, list) else (content, [])
        response = {
            "status": status,
            "result": result,
            "error": ""
        }
    else:
        response = {
            "status": "ERROR",
            "result": [],
            "error": content
        }

    return JsonResponse(response, status=http_status, safe=False)
