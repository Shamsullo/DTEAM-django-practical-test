from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date

from main.models import CV, Project


class ProjectAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cv = CV.objects.create(
            first_name="John",
            last_name="Doe",
            bio="Test Bio"
        )
        self.project = Project.objects.create(
            cv=self.cv,
            title="Test Project",
            description="Test Description",
            start_date=date(2023, 1, 1),
            url="https://example.com"
        )

        # URLs
        self.project_list_url = reverse('cv-projects-list',
                                        kwargs={'cv_pk': self.cv.pk})
        self.project_detail_url = reverse('cv-projects-detail',
                                          kwargs={'cv_pk': self.cv.pk,
                                                  'pk': self.project.pk})

        # Test data
        self.project_data = {
            "title": "New Project",
            "description": "New Description",
            "start_date": "2024-01-01",
            "url": "https://newexample.com"
        }

    def test_create_project(self):
        response = self.client.post(self.project_list_url, self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_get_project_list(self):
        response = self.client.get(self.project_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_project(self):
        response = self.client.delete(self.project_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)
