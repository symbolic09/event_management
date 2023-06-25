from django.test import TestCase
from event_manager.models import Event, Ticket
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from mock import mock
from django.http import JsonResponse
from event_manager import utils
from http import HTTPStatus
import json


class EventTestCase(TestCase):

    def setUp(self) -> None:
        self.timezone = pytz.timezone("Asia/Kolkata")
        self.superuser = User.objects.create_user(
            username='admin', password='Superuser#123', is_superuser=True)
        self.user = User.objects.create_user(
            username='vaibhav', password='normaluser#123')
        self.bday = Event.objects.create(name="Vaibhav's Birthday",
                                         description="Vaibhav's Birthday Bash",
                                         booking_start_datetime=datetime.strptime(
                                             "2023-01-01T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                         booking_end_datetime=datetime.strptime(
                                             "2023-06-12T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                         max_seat=10,
                                         available_seat=10,
                                         event_datetime=datetime.strptime("2023-06-13T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone))
        self.concert = Event.objects.create(name="Metalica Concert",
                                            description="Metalica Concert",
                                            booking_start_datetime=datetime.strptime(
                                                "2023-01-01T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                            booking_end_datetime=datetime.strptime(
                                                "2023-08-13T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                            max_seat=10,
                                            available_seat=0,
                                            event_datetime=datetime.strptime("2023-08-14T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone))
        self.c_2 = Event.objects.create(name="Iron Maiden Concert",
                                        description="Iron Maiden Concert",
                                        booking_start_datetime=datetime.strptime(
                                            "2023-01-01T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                        booking_end_datetime=datetime.strptime(
                                            "2023-08-13T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                        max_seat=10,
                                        available_seat=10,
                                        event_datetime=datetime.strptime("2023-08-14T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone))
        self.prom = Event.objects.create(name="Prom Night",
                                         description="Prom Night",
                                         booking_start_datetime=datetime.strptime(
                                             "2023-10-01T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                         booking_end_datetime=datetime.strptime(
                                             "2023-10-29T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone),
                                         max_seat=10,
                                         available_seat=10,
                                         event_datetime=datetime.strptime("2023-10-30T05:30:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone))
        self.bday_ticket = Ticket.objects.create(event=self.bday,
                                                 user=User.objects.get(
                                                     username="vaibhav"),
                                                 booked_at=datetime(2023, 6, 10, 5, 3, 0, 0, tzinfo=pytz.timezone("Asia/Kolkata")))

    def test_get_all_events(self):
        x = utils.get_all_events()
        self.assertEquals(len(x), 4)

    @mock.patch('django.utils.timezone.now')
    def test_get_live_events(self, mock_datetime):
        mock_datetime.return_value = datetime(
            2023, 6, 25, 5, 3, 0, 0, tzinfo=pytz.timezone("Asia/Kolkata"))
        x = utils.get_live_events()
        self.assertEquals(len(x), 1)

    def test_get_tickets(self):
        x = utils.get_tickets(self.user)
        self.assertEquals(len(x), 1)
        self.assertEquals(x[0].get('id'), 1)

        x = utils.get_tickets(self.user, 1)
        self.assertTrue(isinstance(x, dict))
        self.assertEquals(x.get('id'), 1)

    def test_get_event_detail(self):
        x = utils.get_event_detail(1)
        self.assertEquals(x[0].get('name'), "Vaibhav's Birthday")

        x = utils.get_event_detail(12)
        self.assertEquals(x, [])

    @mock.patch('django.utils.timezone.now')
    def test_try_booking_ticket(self, mock_datetime):

        mock_datetime.return_value = datetime(
            2023, 6, 25, 5, 3, 0, 0, tzinfo=pytz.timezone("Asia/Kolkata"))

        data = {
            "event": self.c_2.id
        }
        x = utils.try_booking_ticket(self.user, data)
        self.assertEquals(x, "BOOKED")

        data = {
            "event": self.concert.id
        }
        x = utils.try_booking_ticket(self.user, data)
        self.assertEquals(x, "NO_SEAT_AVAILABLE")

        data = {
            "event": self.prom.id
        }
        x = utils.try_booking_ticket(self.user, data)
        self.assertEquals(x, "EVENT_BOOKING_UNAVAILABLE")

        data = {
            "event": self.bday.id
        }
        x = utils.try_booking_ticket(self.user, data)
        self.assertEquals(x, "ALREADY_BOOKED")

    def test_create_or_update_event(self):
        data = {
            "name": "Eminem's Concert",
            "description": "Eminem's Concert",
            "booking_start_datetime": "2023-01-01T05:30:00Z",
            "booking_end_datetime": "2023-08-13T05:30:00Z",
            "max_seat": 10,
            "event_datetime": "2023-08-14T05:30:00Z"
        }
        x = utils.create_or_update_event(data)
        self.assertEquals(x, "SUCCESS")

        data = {
            "name": "start > end",
            "description": "start > end",
            "booking_start_datetime": "2023-11-01T05:30:00Z",
            "booking_end_datetime": "2023-08-13T05:30:00Z",
            "max_seat": 10,
            "event_datetime": "2023-08-14T05:30:00Z"
        }
        x = utils.create_or_update_event(data)
        self.assertEquals(x, "VALIDATION_FAILED")

        data = {
            "name": "max seat str",
            "description": "max seat str",
            "booking_start_datetime": "2023-01-01T05:30:00Z",
            "booking_end_datetime": "2023-08-13T05:30:00Z",
            "max_seat": "10",
            "event_datetime": "2023-08-14T05:30:00Z"
        }
        x = utils.create_or_update_event(data)
        self.assertEquals(x, "VALIDATION_FAILED")

        data = {
            "name": "invalide date format",
            "description": "invalide date format",
            "booking_start_datetime": "202-01-01T05:30:00Z",
            "booking_end_datetime": "2023-08-13T05:30:00Z",
            "max_seat": 10,
            "event_datetime": "2023-08-14T05:30:00Z"
        }
        x = utils.create_or_update_event(data)
        self.assertEquals(x, "VALIDATION_FAILED")

    def test_generate_response(self):
        x = utils.generate_response("SUCCESS")
        self.assertTrue(isinstance(x, JsonResponse))

        self.assertDictEqual(
            {"status": "SUCCESS", "result": [], "error": ""}, json.loads((x.content)))

        x = utils.generate_response(["SUCCESS"])
        self.assertDictEqual({"status": "SUCCESS", "result": [
                             "SUCCESS"], "error": ""}, json.loads((x.content)))

        x = utils.generate_response(
            "BAD_REQUEST", is_success=False, http_status=HTTPStatus.BAD_REQUEST)
        self.assertDictEqual({"status": "ERROR", "result": [],
                             "error": "BAD_REQUEST"}, json.loads((x.content)))
