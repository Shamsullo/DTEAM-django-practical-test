from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.models import CV, Contact


class ContactAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Test Bio"
        )
        self.contact = Contact.objects.create(
            cv=self.cv,
            contact_type="EMAIL",
            value="john@example.com",
            is_primary=True,
        )

        # URLs
        self.contact_list_url = reverse(
            "cv-contacts-list", kwargs={"cv_pk": self.cv.pk}
        )
        self.contact_detail_url = reverse(
            "cv-contacts-detail",
            kwargs={"cv_pk": self.cv.pk, "pk": self.contact.pk},
        )

        # Test data
        self.contact_data = {
            "contact_type": "PHONE",
            "value": "+9924567890",
            "is_primary": True,
        }

    def test_create_contact(self):
        response = self.client.post(self.contact_list_url, self.contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)

    def test_get_contact_list(self):
        response = self.client.get(self.contact_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_contact(self):
        response = self.client.put(self.contact_detail_url, self.contact_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Contact.objects.get(id=self.contact.id).value, "+9924567890"
        )
