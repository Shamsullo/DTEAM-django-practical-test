from django.test import TestCase, Client
from django.urls import reverse
from main.models import CV


class CVDetailViewTest(TestCase):
    fixtures = ['cv_sample_data.json']

    def setUp(self):
        self.client = Client()
        self.cv = CV.objects.first()

    def test_cv_detail_view(self):
        response = self.client.get(
            reverse('cv_detail', kwargs={'pk': self.cv.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cv_detail.html')

        self.assertEqual(response.context['cv'], self.cv)

        self.assertTrue(len(response.context['cv'].skills.all()) > 0)
        self.assertTrue(len(response.context['cv'].projects.all()) > 0)
        self.assertTrue(len(response.context['cv'].contacts.all()) > 0)

    def test_cv_detail_view_404(self):
        response = self.client.get(
            reverse('cv_detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)