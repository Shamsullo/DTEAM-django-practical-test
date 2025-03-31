from django.test import TestCase, Client
from django.urls import reverse


class CVListViewTest(TestCase):
    fixtures = ["cv_sample_data.json"]

    def setUp(self):
        self.client = Client()

    def test_cv_list_view(self):
        response = self.client.get(reverse("cv_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cv_list.html")

        self.assertTrue("cvs" in response.context)

        first_cv = response.context["cvs"][0]
        self.assertEqual(first_cv.first_name, "Shamsullo")
        self.assertEqual(first_cv.last_name, "Ismatov")

        with self.assertNumQueries(0):
            skills = list(first_cv.skills.all())
            projects = list(first_cv.projects.all())
            contacts = list(first_cv.contacts.all())
