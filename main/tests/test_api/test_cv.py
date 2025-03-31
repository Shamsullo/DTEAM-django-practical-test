from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date

from main.models import CV, Contact, Skill, Project


class CVAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a base CV for testing related models
        self.cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Test Bio"
        )

        # Base URLs
        self.cv_list_url = reverse("cv-list")
        self.cv_detail_url = reverse("cv-detail", kwargs={"pk": self.cv.pk})

        # Base data for testing
        self.cv_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "bio": "Test Bio",
        }

    def test_create_cv(self):
        response = self.client.post(self.cv_list_url, self.cv_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)
        self.assertEqual(CV.objects.latest("id").first_name, "Jane")

    def test_get_cv_list(self):
        response = self.client.get(self.cv_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_cv_detail(self):
        response = self.client.get(self.cv_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")

    def test_update_cv(self):
        response = self.client.put(self.cv_detail_url, self.cv_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CV.objects.get(id=self.cv.id).first_name, "Jane")

    def test_delete_cv(self):
        response = self.client.delete(self.cv_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)


class CVDetailAPITests(TestCase):
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
        self.skill = Skill.objects.create(
            cv=self.cv, name="Python", proficiency="ADV"
        )
        self.project = Project.objects.create(
            cv=self.cv,
            title="Test Project",
            description="Test Description",
            start_date=date(2023, 1, 1),
            url="https://example.com",
        )

        self.cv_detail_url = reverse("cv-detail", kwargs={"pk": self.cv.pk})

    def test_get_cv_with_related_data(self):
        response = self.client.get(self.cv_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that all related data is included
        self.assertEqual(len(response.data["contacts"]), 1)
        self.assertEqual(len(response.data["skills"]), 1)
        self.assertEqual(len(response.data["projects"]), 1)

        # Verify content
        self.assertEqual(
            response.data["contacts"][0]["value"], "john@example.com"
        )
        self.assertEqual(response.data["skills"][0]["name"], "Python")
        self.assertEqual(response.data["projects"][0]["title"], "Test Project")
