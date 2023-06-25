from oauth2_provider.views import ReadWriteScopedResourceView
from django.http import JsonResponse
from http import HTTPStatus

import json
from .utils import get_live_events, try_booking_ticket, get_all_events, generate_response, get_event_detail, create_or_update_event, get_tickets


class EventView(ReadWriteScopedResourceView):

    def get(self, requests):
        return generate_response(get_all_events() if requests.user.is_superuser else get_live_events())

    def post(self, requests):
        if requests.user.is_superuser:
            event_status = create_or_update_event(json.loads(requests.body))
            status = event_status == "SUCCESS"
            return generate_response(event_status, status, http_status=HTTPStatus.CREATED if status else HTTPStatus.UNPROCESSABLE_ENTITY)
        else:
            return generate_response("You don't have access for this API", False, http_status=HTTPStatus.FORBIDDEN)

    def put(self, requests):
        if requests.user.is_superuser:
            event_status = create_or_update_event(json.loads(requests.body))
            status = event_status == "SUCCESS"
            return generate_response(event_status, status, http_status=HTTPStatus.OK if status else HTTPStatus.UNPROCESSABLE_ENTITY)
        else:
            return generate_response("You don't have access for this API", False, http_status=HTTPStatus.FORBIDDEN)


class EventSummaryView(ReadWriteScopedResourceView):

    def get(self, requests, event_id):
        if not requests.user.is_superuser:
            return generate_response("You don't have access for this API", False, http_status=HTTPStatus.FORBIDDEN)
        return generate_response(get_event_detail(event_id))


class TicketView(ReadWriteScopedResourceView):

    def get(self, requests, ticket_id=None):
        return generate_response(get_tickets(requests.user, ticket_id))

    def post(self, requests):
        data = json.loads(requests.body)
        if 'event' not in data.keys():
            return generate_response("event is missing", False, http_status=HTTPStatus.BAD_REQUEST)
        return generate_response(try_booking_ticket(requests.user, data))
