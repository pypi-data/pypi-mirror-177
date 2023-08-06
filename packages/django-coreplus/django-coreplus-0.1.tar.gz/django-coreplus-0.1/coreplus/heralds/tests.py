import json
from io import BytesIO

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import tag
from rest_framework.test import APILiveServerTestCase, APITestCase

from coreplus.reactions.models import Reaction

from .models import DirectMessage


class HeraldApiTest(APILiveServerTestCase):
    BASE_URL = "/api/v1/heralds"

    # TODO: Buat fitur user untuk matiin notifikasi
    # TODO: Buat notifikasi ke user yang diundang ke club
    # TODO: Buat notifikasi untuk owner club jika ada user yang mau join
    # TODO: Buat notifikasi kalau status invitation berubah (di accept atau reject)
    # TODO: Buat notifikasi kalau ada reply, discuss, reaction
    # TODO: Buat notifikasi ke club owner untuk user yang join

    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test",
            email="test@yopmail.com",
            password="testpassword",
        )
        self.user.save()
        self.recipient = User.objects.create_user(
            username="recipient",
            email="recipient@yopmail.com",
            password="recipientpassword",
        )
        self.recipient.save()
        self.direct_message = DirectMessage(
            sender=self.user,
            recipient=self.recipient,
            status="unread",
            content="This is a test direct message",
        )
        self.direct_message.save()
        return super().setUp()

    @tag("heralds_api_v1_endpoint")
    def test_direct_message_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.BASE_URL}/direct-message/")
        self.assertEqual(response.status_code, 200)

    @tag("heralds_api_v1_endpoint", "heralds_api_v1_endpoint_test")
    def test_create_direct_message(self):
        data = {
            "recipient": self.recipient.id,
            "content": "This is a test direct message",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"{self.BASE_URL}/direct-message/", data)
        self.assertEqual(response.status_code, 201)

    @tag("heralds_api_v1_endpoint")
    def test_get_recipient_message_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f"{self.BASE_URL}/direct-message/get-recipient/{self.recipient.username}/"
        )
        self.assertEqual(response.status_code, 200)

    @tag("heralds_api_v1_endpoint", "heralds_api_v1_endpoint_test")
    def test_create_and_delete_direct_message_with_attachment(self):
        img = BytesIO(b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00")
        img.name = "image.png"
        data = {"file": img}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/v1/media/image/", data)
        self.assertEqual(response.status_code, 201)
        jsonResponse = json.loads(response.content)
        attachment_id = jsonResponse.get("id")

        data = {
            "recipient": self.recipient.id,
            "content": "This is a test direct message",
            "attachment_ids": [attachment_id],
        }
        response = self.client.post(
            f"{self.BASE_URL}/direct-message/",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertContains(response, f'"attachment":{attachment_id}', status_code=201)
        filer_model = django_apps.get_model(
            settings.FILER_IMAGE_MODEL, require_ready=False
        )
        file_count = filer_model.objects.all().count()
        self.assertEqual(file_count, 1)

        # Delete the direct message
        jsonResponse = json.loads(response.content)
        message_id = jsonResponse.get("id")
        self.client.delete(f"{self.BASE_URL}/direct-message/{message_id}/")
        file_count = filer_model.objects.all().count()
        self.assertEqual(file_count, 0)

    @tag("heralds_api_v1_endpoint")
    def test_get_user_reaction(self):
        self.client.force_authenticate(user=self.user)
        self.direct_message.add_reaction(self.user, Reaction.LIKE)
        self.direct_message.save()
        response = self.client.get(
            f"{self.BASE_URL}/direct-message/{self.direct_message.id}/reaction/"
        )
        self.assertContains(response, '"value":"like"')

    @tag("heralds_api_v1_endpoint")
    def test_direct_message_add_reaction(self):
        data = {"value": "like"}
        self.client.force_authenticate(user=self.user)
        self.client.post(
            f"{self.BASE_URL}/direct-message/{self.direct_message.id}/add-reaction/",
            data,
        )
        self.direct_message.save()

        reaction_like = self.direct_message.reactions.filter(
            value=Reaction.LIKE
        ).count()
        self.assertEqual(reaction_like, 1)
        self.assertEqual(self.direct_message.reaction, {"like": 1})

    @tag("heralds_api_v1_endpoint")
    def test_direct_message_update_reaction(self):
        self.direct_message.add_reaction(self.user, Reaction.LIKE)
        self.direct_message.save()
        data = {"value": "love"}
        self.client.force_authenticate(user=self.user)
        self.client.post(
            f"{self.BASE_URL}/direct-message/{self.direct_message.id}/add-reaction/",
            data,
        )
        self.direct_message.save()

        reaction_love = self.direct_message.reactions.filter(
            value=Reaction.LOVE
        ).count()
        self.assertEqual(reaction_love, 1)
        self.assertEqual(self.direct_message.reaction, {"love": 1})

    @tag("heralds_api_v1_endpoint")
    def test_direct_message_delete_reaction(self):
        self.direct_message.add_reaction(self.user, Reaction.LIKE)
        self.direct_message.save()
        reaction_like = self.direct_message.reactions.filter(
            value=Reaction.LIKE
        ).count()
        self.assertEqual(reaction_like, 1)

        self.client.force_authenticate(user=self.user)
        self.client.delete(
            f"{self.BASE_URL}/direct-message/{self.direct_message.id}/delete-reaction/"
        )
        self.direct_message.save()

        reaction_like = self.direct_message.reactions.filter(
            value=Reaction.LIKE
        ).count()
        self.assertEqual(reaction_like, 0)
        self.assertEqual(self.direct_message.reaction, {})


class HeraldsTest(APITestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.sender = User.objects.create_user(
            username="sender", email="sender@yopmail.com", password="senderpassword"
        )
        self.sender.save()
        self.recipient = User.objects.create_user(
            username="recipient",
            email="recipient@yopmail.com",
            password="recipientpassword",
        )
        self.recipient.save()
        return super().setUp()

    @tag("heralds_unit_test")
    def test_create_direct_message(self):
        direct_message = DirectMessage(
            sender=self.sender,
            recipient=self.recipient,
            content="this is a test direct message",
            status="unread",
        )
        direct_message.save()

        total_messages = DirectMessage.objects.all().count()
        messages = DirectMessage.objects.get(id=direct_message.id)

        self.assertEqual(total_messages, 1)
        self.assertEqual(messages.content, "this is a test direct message")
