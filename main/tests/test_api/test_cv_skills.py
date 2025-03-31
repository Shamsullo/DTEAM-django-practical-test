from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.models import CV, Skill


class SkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Test Bio"
        )
        self.skill = Skill.objects.create(
            cv=self.cv, name="Python", proficiency="ADV"
        )

        # URLs
        self.skill_list_url = reverse(
            "cv-skills-list", kwargs={"cv_pk": self.cv.pk}
        )
        self.skill_detail_url = reverse(
            "cv-skills-detail",
            kwargs={"cv_pk": self.cv.pk, "pk": self.skill.pk},
        )

        # Test data
        self.skill_data = {"name": "JavaScript", "proficiency": "INT"}

    def test_create_skill(self):
        response = self.client.post(self.skill_list_url, self.skill_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)

    def test_get_skill_list(self):
        response = self.client.get(self.skill_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
